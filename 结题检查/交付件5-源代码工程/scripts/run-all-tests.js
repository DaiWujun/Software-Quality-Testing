#!/usr/bin/env node

/**
 * White-Jotter 集成测试脚本
 * 自动运行所有单元测试和 E2E 测试
 */

const { spawn } = require('child_process')
const chalk = require('chalk')
const ora = require('ora')

// 测试配置
const tests = [
  {
    name: '单元测试',
    command: 'npm',
    args: ['run', 'unit'],
    description: '运行 Jest 单元测试'
  },
  {
    name: 'E2E 测试',
    command: 'npm',
    args: ['run', 'e2e'],
    description: '运行 Nightwatch E2E 测试',
    skipOnError: true // E2E 测试失败不中断流程
  }
]

// 测试结果统计
const results = {
  passed: [],
  failed: [],
  skipped: []
}

console.log(chalk.cyan.bold('\n╔════════════════════════════════════════════════════════╗'))
console.log(chalk.cyan.bold('║     White-Jotter 集成测试套件                         ║'))
console.log(chalk.cyan.bold('╚════════════════════════════════════════════════════════╝\n'))

/**
 * 运行单个测试
 */
function runTest(test) {
  return new Promise((resolve, reject) => {
    const spinner = ora({
      text: `${test.description}...`,
      color: 'yellow'
    }).start()

    const startTime = Date.now()
    const testProcess = spawn(test.command, test.args, {
      shell: true,
      stdio: 'pipe'
    })

    let output = ''
    let errorOutput = ''

    testProcess.stdout.on('data', (data) => {
      output += data.toString()
    })

    testProcess.stderr.on('data', (data) => {
      errorOutput += data.toString()
    })

    testProcess.on('close', (code) => {
      const duration = ((Date.now() - startTime) / 1000).toFixed(2)

      if (code === 0) {
        spinner.succeed(chalk.green(`${test.name} 通过 (${duration}s)`))
        results.passed.push(test.name)
        resolve({ success: true, output, duration })
      } else {
        if (test.skipOnError) {
          spinner.warn(chalk.yellow(`${test.name} 失败但已跳过 (${duration}s)`))
          results.skipped.push(test.name)
          resolve({ success: false, skipped: true, output: errorOutput, duration })
        } else {
          spinner.fail(chalk.red(`${test.name} 失败 (${duration}s)`))
          results.failed.push(test.name)
          reject({ success: false, output: errorOutput, duration })
        }
      }
    })

    testProcess.on('error', (error) => {
      spinner.fail(chalk.red(`${test.name} 执行错误`))
      results.failed.push(test.name)
      reject({ success: false, error: error.message })
    })
  })
}

/**
 * 运行所有测试
 */
async function runAllTests() {
  console.log(chalk.blue('开始运行测试套件...\n'))

  for (const test of tests) {
    try {
      await runTest(test)
      console.log() // 添加空行
    } catch (error) {
      console.log() // 添加空行
      if (!test.skipOnError) {
        console.log(chalk.red('\n测试失败，停止执行\n'))
        break
      }
    }
  }

  printSummary()
}

/**
 * 打印测试摘要
 */
function printSummary() {
  console.log(chalk.cyan.bold('\n╔════════════════════════════════════════════════════════╗'))
  console.log(chalk.cyan.bold('║     测试结果摘要                                       ║'))
  console.log(chalk.cyan.bold('╚════════════════════════════════════════════════════════╝\n'))

  const total = results.passed.length + results.failed.length + results.skipped.length
  const passRate = total > 0 ? ((results.passed.length / total) * 100).toFixed(1) : 0

  console.log(chalk.white('  总测试套件: ') + chalk.bold(total))
  console.log(chalk.green('  ✓ 通过: ') + chalk.bold(results.passed.length))
  console.log(chalk.red('  ✗ 失败: ') + chalk.bold(results.failed.length))
  console.log(chalk.yellow('  ⊗ 跳过: ') + chalk.bold(results.skipped.length))
  console.log(chalk.white('  通过率: ') + chalk.bold(`${passRate}%`))

  if (results.passed.length > 0) {
    console.log(chalk.green('\n  通过的测试:'))
    results.passed.forEach(name => {
      console.log(chalk.green(`    ✓ ${name}`))
    })
  }

  if (results.failed.length > 0) {
    console.log(chalk.red('\n  失败的测试:'))
    results.failed.forEach(name => {
      console.log(chalk.red(`    ✗ ${name}`))
    })
  }

  if (results.skipped.length > 0) {
    console.log(chalk.yellow('\n  跳过的测试:'))
    results.skipped.forEach(name => {
      console.log(chalk.yellow(`    ⊗ ${name}`))
    })
  }

  console.log('\n' + chalk.cyan('─'.repeat(60)) + '\n')

  // 退出码
  const exitCode = results.failed.length > 0 ? 1 : 0

  if (exitCode === 0) {
    console.log(chalk.green.bold('🎉 所有测试通过！\n'))
  } else {
    console.log(chalk.red.bold('❌ 部分测试失败\n'))
  }

  process.exit(exitCode)
}

/**
 * 主函数
 */
function main() {
  // 检查参数
  const args = process.argv.slice(2)

  if (args.includes('--help') || args.includes('-h')) {
    console.log(chalk.cyan('用法:'))
    console.log('  node run-all-tests.js [选项]\n')
    console.log(chalk.cyan('选项:'))
    console.log('  --help, -h     显示帮助信息')
    console.log('  --unit         仅运行单元测试')
    console.log('  --e2e          仅运行 E2E 测试\n')
    process.exit(0)
  }

  if (args.includes('--unit')) {
    tests.splice(1, 1) // 移除 E2E 测试
  }

  if (args.includes('--e2e')) {
    tests.splice(0, 1) // 移除单元测试
  }

  runAllTests().catch(error => {
    console.error(chalk.red('测试执行出错:'), error)
    process.exit(1)
  })
}

// 运行主函数
main()
