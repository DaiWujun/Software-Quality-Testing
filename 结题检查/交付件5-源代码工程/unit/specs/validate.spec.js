import {
  isExternal,
  validUsername,
  validURL,
  validLowerCase,
  validUpperCase,
  validAlphabets,
  validEmail,
  isString,
  isArray
} from '@/utils/validate'

describe('Utils:validate', () => {
  describe('isExternal', () => {
    it('应该识别外部链接', () => {
      expect(isExternal('https://example.com')).toBe(true)
      expect(isExternal('http://example.com')).toBe(true)
      expect(isExternal('mailto:test@example.com')).toBe(true)
      expect(isExternal('tel:1234567890')).toBe(true)
    })

    it('应该识别内部链接', () => {
      expect(isExternal('/dashboard')).toBe(false)
      expect(isExternal('./dashboard')).toBe(false)
      expect(isExternal('dashboard')).toBe(false)
    })
  })

  describe('validUsername', () => {
    it('应该验证有效的用户名', () => {
      expect(validUsername('admin')).toBe(true)
      expect(validUsername('editor')).toBe(true)
      expect(validUsername(' admin ')).toBe(true) // 带空格也能通过trim
    })

    it('应该拒绝无效的用户名', () => {
      expect(validUsername('user')).toBe(false)
      expect(validUsername('test')).toBe(false)
      expect(validUsername('')).toBe(false)
    })
  })

  describe('validURL', () => {
    it('应该验证有效的URL', () => {
      expect(validURL('https://www.example.com')).toBe(true)
      expect(validURL('http://example.com')).toBe(true)
      expect(validURL('ftp://files.example.com')).toBe(true)
      expect(validURL('https://example.com/path/to/page')).toBe(true)
      expect(validURL('http://192.168.1.1')).toBe(true)
    })

    it('应该拒绝无效的URL', () => {
      expect(validURL('example.com')).toBe(false)
      expect(validURL('not a url')).toBe(false)
      expect(validURL('')).toBe(false)
      expect(validURL('javascript:alert(1)')).toBe(false)
    })
  })

  describe('validLowerCase', () => {
    it('应该验证全小写字符串', () => {
      expect(validLowerCase('abc')).toBe(true)
      expect(validLowerCase('abcdefghijklmnopqrstuvwxyz')).toBe(true)
    })

    it('应该拒绝非全小写字符串', () => {
      expect(validLowerCase('Abc')).toBe(false)
      expect(validLowerCase('ABC')).toBe(false)
      expect(validLowerCase('abc123')).toBe(false)
      expect(validLowerCase('abc def')).toBe(false)
      expect(validLowerCase('')).toBe(false)
    })
  })

  describe('validUpperCase', () => {
    it('应该验证全大写字符串', () => {
      expect(validUpperCase('ABC')).toBe(true)
      expect(validUpperCase('ABCDEFGHIJKLMNOPQRSTUVWXYZ')).toBe(true)
    })

    it('应该拒绝非全大写字符串', () => {
      expect(validUpperCase('Abc')).toBe(false)
      expect(validUpperCase('abc')).toBe(false)
      expect(validUpperCase('ABC123')).toBe(false)
      expect(validUpperCase('ABC DEF')).toBe(false)
      expect(validUpperCase('')).toBe(false)
    })
  })

  describe('validAlphabets', () => {
    it('应该验证纯字母字符串', () => {
      expect(validAlphabets('abc')).toBe(true)
      expect(validAlphabets('ABC')).toBe(true)
      expect(validAlphabets('AbCdEf')).toBe(true)
    })

    it('应该拒绝包含非字母的字符串', () => {
      expect(validAlphabets('abc123')).toBe(false)
      expect(validAlphabets('abc def')).toBe(false)
      expect(validAlphabets('abc-def')).toBe(false)
      expect(validAlphabets('')).toBe(false)
      expect(validAlphabets('123')).toBe(false)
    })
  })

  describe('validEmail', () => {
    it('应该验证有效的邮箱地址', () => {
      expect(validEmail('test@example.com')).toBe(true)
      expect(validEmail('user.name@example.com')).toBe(true)
      expect(validEmail('user+tag@example.co.uk')).toBe(true)
      expect(validEmail('test123@test-domain.com')).toBe(true)
    })

    it('应该拒绝无效的邮箱地址', () => {
      expect(validEmail('invalid')).toBe(false)
      expect(validEmail('@example.com')).toBe(false)
      expect(validEmail('test@')).toBe(false)
      expect(validEmail('test @example.com')).toBe(false)
      expect(validEmail('')).toBe(false)
      expect(validEmail('test')).toBe(false)
    })
  })

  describe('isString', () => {
    it('应该识别字符串', () => {
      expect(isString('hello')).toBe(true)
      expect(isString('')).toBe(true)
      expect(isString(String('hello'))).toBe(true)
      expect(isString(new String('hello'))).toBe(true)
    })

    it('应该识别非字符串', () => {
      expect(isString(123)).toBe(false)
      expect(isString(true)).toBe(false)
      expect(isString(null)).toBe(false)
      expect(isString(undefined)).toBe(false)
      expect(isString({})).toBe(false)
      expect(isString([])).toBe(false)
    })
  })

  describe('isArray', () => {
    it('应该识别数组', () => {
      expect(isArray([])).toBe(true)
      expect(isArray([1, 2, 3])).toBe(true)
      expect(isArray(new Array())).toBe(true)
    })

    it('应该识别非数组', () => {
      expect(isArray('array')).toBe(false)
      expect(isArray(123)).toBe(false)
      expect(isArray(true)).toBe(false)
      expect(isArray(null)).toBe(false)
      expect(isArray(undefined)).toBe(false)
      expect(isArray({})).toBe(false)
    })
  })
})
