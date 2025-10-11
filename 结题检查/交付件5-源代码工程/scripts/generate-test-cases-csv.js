/*
  Generate a consolidated CSV of all test cases (unit + e2e).
  Columns:
  Test Case ID, Test Item, Test Case Title, Test Criticality, Pre-condition, Input, Procedure, Output, Result, Status, Remark
*/

const fs = require('fs')
const path = require('path')

const ROOT = path.resolve(__dirname, '..')
const UNIT_DIR = path.join(ROOT, 'test', 'unit', 'specs')
const E2E_DIR = path.join(ROOT, 'test', 'e2e', 'specs')
const OUT_FILE = path.join(ROOT, 'TEST_CASES_FULL.csv')
const JEST_JSON_FILE = path.join(ROOT, 'test', 'unit', 'jest-result.json')

function listFilesRecursively(dir) {
  if (!fs.existsSync(dir)) return []
  const entries = fs.readdirSync(dir, { withFileTypes: true })
  const files = []
  for (const e of entries) {
    const full = path.join(dir, e.name)
    if (e.isDirectory()) files.push(...listFilesRecursively(full))
    else if (e.isFile()) files.push(full)
  }
  return files
}

function readFileSafe(p) {
  try { return fs.readFileSync(p, 'utf8') } catch { return '' }
}

function sanitize(text) {
  if (text == null) return ''
  // Remove CRLF newlines and quotes for CSV safety; wrap later with quotes
  return String(text).replace(/\r?\n/g, ' ').replace(/"/g, '""').trim()
}

function joinCsvRow(cells) {
  return cells.map(v => `"${sanitize(v)}"`).join(',')
}

function inferCriticality(item, title, filePath, type) {
  const s = `${item} ${title} ${filePath}`.toLowerCase()
  if (/login|\u767b\u5f55|admin|dashboard/.test(s)) return 'High'
  if (/navigation|navigate|\u5bfc\u822a|router/.test(s)) return 'Medium'
  if (/error|fail|\u5931\u8d25/.test(s)) return 'Medium'
  if (type === 'e2e') return 'High'
  if (/utils|validate/.test(filePath)) return 'Medium'
  if (/basic|env|\u73af\u5883/.test(s)) return 'Low'
  return 'Medium'
}

function defaultPrecondition(type, filePath) {
  if (type === 'unit') {
    const base = 'Jest + @vue/test-utils 环境，axios 已 mock（见 test/unit/setup.js）'
    if (/Login|Register|Books|Articles|Admin/i.test(filePath)) {
      return base + '；Vue Router/Vuex 已在 localVue 中注册（按测试文件 beforeEach）'
    }
    return base
  }
  return 'Nightwatch + Selenium + ChromeDriver；需要本地 dev server (npm run dev) 可访问'
}

function defaultRemark(type, filePath) {
  if (type === 'unit') {
    return '@vue/test-utils + Jest（axios.mockResolvedValue / mount or shallowMount）'
  }
  return 'Nightwatch E2E（browser.* 流程断言）'
}

function buildUnitCases() {
  const files = listFilesRecursively(UNIT_DIR).filter(f => f.endsWith('.spec.js'))
  const cases = []
  for (const file of files) {
    const content = readFileSafe(file)
    if (!content) continue

    // Pre-collect all describe titles with positions
    const describeRegex = /describe\(\s*([`'\"])(.*?)\1\s*,\s*\(/g
    const describes = []
    let dm
    while ((dm = describeRegex.exec(content)) !== null) {
      describes.push({ title: dm[2], index: dm.index })
    }

    // Collect it() titles with positions
    const itRegex = /it\(\s*([`'\"])(.*?)\1\s*,\s*(async\s*)?\(.*?\)\s*=>|it\(\s*([`'\"])(.*?)\4\s*,\s*function\s*\(/gms
    // Simpler: two-pass for common forms: it('...'
    const itSimple = /it\(\s*([`'\"])(.*?)\1\s*,/g
    let im
    while ((im = itSimple.exec(content)) !== null) {
      const title = im[2]
      const pos = im.index
      // find nearest 1-2 describes before this it
      const ctx = describes.filter(d => d.index < pos).slice(-2).map(d => d.title)
      const testItem = ctx.length ? ctx.join(' > ') : path.basename(file)
      const criticality = inferCriticality(testItem, title, file, 'unit')
      const pre = defaultPrecondition('unit', file)

      cases.push({
        type: 'unit',
        file,
        item: testItem,
        title,
        criticality,
        precondition: pre,
        input: '按测试中 mount/setData/mock 配置',
        procedure: '挂载组件，执行交互或调用方法，断言预期',
        output: '断言通过（expect 条件满足）',
        result: '未执行（生成时）',
        status: 'Unknown',
        remark: defaultRemark('unit', file)
      })
    }
  }
  return cases
}

function buildE2ECases() {
  const files = listFilesRecursively(E2E_DIR).filter(f => f.endsWith('.test.js'))
  const cases = []
  for (const file of files) {
    const content = readFileSafe(file)
    if (!content) continue
    const entryRegex = /['\"]([^'\"]+)['\"]\s*:\s*function\s*\(browser\)/g
    let m
    while ((m = entryRegex.exec(content)) !== null) {
      const title = m[1]
      const item = `E2E: ${path.basename(file)}`
      const criticality = inferCriticality(item, title, file, 'e2e')
      cases.push({
        type: 'e2e',
        file,
        item,
        title,
        criticality,
        precondition: defaultPrecondition('e2e', file),
        input: '浏览器访问指定 URL，按脚本设置输入/点击',
        procedure: 'Nightwatch 按步骤执行浏览器操作并断言',
        output: '期望的元素/URL 断言成立',
        result: '未执行（无 dev server 或未运行 E2E）',
        status: '未执行',
        remark: defaultRemark('e2e', file)
      })
    }
  }
  return cases
}

function loadJestResults() {
  if (!fs.existsSync(JEST_JSON_FILE)) return null
  try {
    const json = JSON.parse(fs.readFileSync(JEST_JSON_FILE, 'utf8'))
    const map = new Map()
    const baseMap = new Map() // key: basename::title
    // json.testResults: array per file
    for (const tr of json.testResults || []) {
      const filePath = tr.name || tr.testFilePath || ''
      for (const a of tr.assertionResults || []) {
        const key = `${path.normalize(filePath)}::${a.title}`
        const val = {
          status: a.status, // passed | failed | pending
          failureMessages: a.failureMessages || []
        }
        map.set(key, val)
        const bkey = `${path.basename(filePath)}::${a.title}`
        if (!baseMap.has(bkey)) baseMap.set(bkey, val)
      }
    }
    return { map, baseMap }
  } catch (e) {
    return null
  }
}

function writeCsv(cases) {
  // Assign IDs
  let unitIdx = 1, e2eIdx = 1
  for (const c of cases) {
    if (c.type === 'unit') c.id = `UNIT-${String(unitIdx++).padStart(3, '0')}`
    else c.id = `E2E-${String(e2eIdx++).padStart(3, '0')}`
  }

  // Try load Jest results to enrich unit cases status/result
  const jest = loadJestResults()
  if (jest) {
    for (const c of cases) {
      if (c.type !== 'unit') continue
      // Try to match by absolute path in jest result map
      const absKey = `${path.normalize(c.file)}::${c.title}`
      const baseKey = `${path.basename(c.file)}::${c.title}`
      let hit = null
      if (jest.map.has(absKey)) hit = jest.map.get(absKey)
      else if (jest.baseMap.has(baseKey)) hit = jest.baseMap.get(baseKey)
      if (hit) {
        if (hit.status === 'passed') {
          c.status = '通过'
          c.result = '与预期一致（单元测试通过）'
        } else if (hit.status === 'failed') {
          c.status = '失败'
          const msg = (hit.failureMessages[0] || '').split('\n')[0]
          c.result = msg || '断言失败'
        } else if (hit.status === 'pending') {
          c.status = '跳过'
          c.result = '测试被跳过'
        }
      }
    }
  }

  const header = [
    'Test Case ID 测试用例编号',
    'Test Item 测试项（即功能模块或函数）',
    'Test Case Title 测试用例标题',
    'Test Criticality重要级别',
    'Pre-condition 预置条件',
    'Input 输入',
    'Procedure 操作步骤',
    'Output 预期结果',
    'Result 实际结果',
    'Status 是否通过',
    'Remark 备注（在此描述使用的测试方法）'
  ]

  const rows = [joinCsvRow(header)]
  for (const c of cases) {
    rows.push(joinCsvRow([
      c.id,
      c.item,
      c.title,
      c.criticality,
      c.precondition,
      c.input,
      c.procedure,
      c.output,
      c.result,
      c.status,
      c.remark
    ]))
  }

  fs.writeFileSync(OUT_FILE, rows.join('\n'), 'utf8')
  return OUT_FILE
}

function main() {
  const unitCases = buildUnitCases()
  const e2eCases = buildE2ECases()
  const all = [...unitCases, ...e2eCases]
  const out = writeCsv(all)
  console.log(`[ok] Generated: ${path.relative(ROOT, out)} (cases: ${all.length})`)
}

if (require.main === module) {
  main()
}
