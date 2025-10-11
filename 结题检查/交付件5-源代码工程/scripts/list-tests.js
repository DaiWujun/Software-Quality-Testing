const fs = require('fs');
const path = require('path');

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walk(fullPath));
    } else if (fullPath.endsWith('.spec.js') || fullPath.endsWith('.test.js')) {
      files.push(fullPath);
    }
  }
  return files;
}

const root = path.join(process.cwd(), 'test');
const files = walk(root);
const cases = [];

for (const file of files) {
  const content = fs.readFileSync(file, 'utf8');
  const relative = path.relative(process.cwd(), file).replace(/\\/g, '/');
  const isE2E = relative.startsWith('test/e2e/specs/');

  if (isE2E) {
    const exportRegex = /['"]([^'"\\]+)['"]\s*:\s*function/g;
    let match;
    while ((match = exportRegex.exec(content)) !== null) {
      cases.push({
        file: relative,
        describe: 'Nightwatch Suite',
        test: match[1],
        type: 'e2e'
      });
    }
    continue;
  }

  const describeRegex = /describe\s*\(\s*['"]([^'"\\]+)['"]/g;
  const describes = [];
  let match;
  while ((match = describeRegex.exec(content)) !== null) {
    describes.push({ name: match[1], index: match.index });
  }

  const itRegex = /(?:it|test)\s*\(\s*['"]([^'"\\]+)['"]/g;
  while ((match = itRegex.exec(content)) !== null) {
    const describe = describes.filter((d) => d.index < match.index).pop();
    cases.push({
      file: relative,
      describe: describe ? describe.name : '(root)',
      test: match[1],
      type: 'unit'
    });
  }
}

const criticalHighKeywords = ['login', 'logout', 'admin', 'dashboard', '认证', '权限', '登录', '注册'];

const rows = cases.map((testCase, index) => {
  const id = `TC-${String(index + 1).padStart(3, '0')}`;
  const lowerTitle = testCase.test.toLowerCase();
  const criticality = criticalHighKeywords.some((k) => lowerTitle.includes(k)) ? 'High' : 'Medium';
  const isE2E = testCase.type === 'e2e';
  const precondition = isE2E
    ? 'Nightwatch + Selenium 测试环境已启动，前端开发服务器可访问'
    : 'Jest 测试环境已初始化，相关组件与依赖已被 stub/mock';
  const input = isE2E
    ? '按照测试脚本模拟浏览器输入、点击与导航操作'
    : '根据用例在组件实例上设置数据、调用方法或触发事件';
  const procedure = isE2E
    ? `执行 Nightwatch 用例 "${testCase.test}"（文件 ${testCase.file}）`
    : `执行 Jest 用例 "${testCase.test}"（文件 ${testCase.file}）`;
  const output = isE2E
    ? '浏览器断言通过，页面行为满足预期'
    : '断言通过，组件状态或输出满足预期';
  const result = '未执行（汇总用例）';
  const status = 'Not Run';
  const remark = isE2E
    ? '自动化端到端测试（Nightwatch + Selenium）'
    : '@vue/test-utils + Jest 自动化单元测试';

  const escape = (value) => String(value).replace(/\|/g, '\\|');

  return [
    id,
    escape(testCase.describe),
    escape(testCase.test),
    criticality,
    escape(precondition),
    escape(input),
    escape(procedure),
    escape(output),
    result,
    status,
    escape(remark)
  ].join(' | ');
});

const header = [
  'Test Case ID',
  'Test Item',
  'Test Case Title',
  'Test Criticality',
  'Pre-condition',
  'Input',
  'Procedure',
  'Output',
  'Result',
  'Status',
  'Remark'
].join(' | ');

const separator = new Array(11).fill('---').join(' | ');

const markdown = [header, separator, ...rows].join('\n');

const outputPath = path.join(process.cwd(), 'TEST_CASES_TABLE.md');
fs.writeFileSync(outputPath, markdown, 'utf8');

console.log(`Generated ${cases.length} test case rows in TEST_CASES_TABLE.md`);
