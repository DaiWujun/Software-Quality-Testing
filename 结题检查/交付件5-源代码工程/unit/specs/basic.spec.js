/**
 * 简单的测试示例 - 用于验证测试环境配置
 */

describe('测试环境验证', () => {
  it('应该能够运行基本的测试', () => {
    expect(true).toBe(true)
  })

  it('应该能够进行数学运算', () => {
    const sum = 1 + 1
    expect(sum).toBe(2)
  })

  it('应该能够测试数组', () => {
    const arr = [1, 2, 3]
    expect(arr).toHaveLength(3)
    expect(arr).toContain(2)
  })

  it('应该能够测试对象', () => {
    const obj = { name: 'test', value: 123 }
    expect(obj).toHaveProperty('name')
    expect(obj.name).toBe('test')
  })

  it('应该能够测试异步代码', async () => {
    const promise = Promise.resolve('success')
    const result = await promise
    expect(result).toBe('success')
  })
})

describe('localStorage mock 测试', () => {
  beforeEach(() => {
    // 清空 mock
    localStorage.setItem.mockClear()
    localStorage.getItem.mockClear()
    localStorage.removeItem.mockClear()
  })

  it('应该能够 mock localStorage.setItem', () => {
    localStorage.setItem('key', 'value')
    expect(localStorage.setItem).toHaveBeenCalledWith('key', 'value')
  })

  it('应该能够 mock localStorage.getItem', () => {
    localStorage.getItem.mockReturnValue('test value')
    const value = localStorage.getItem('key')
    expect(value).toBe('test value')
  })

  it('应该能够 mock localStorage.removeItem', () => {
    localStorage.removeItem('key')
    expect(localStorage.removeItem).toHaveBeenCalledWith('key')
  })
})
