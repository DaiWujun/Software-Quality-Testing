// E2E 测试: 登录流程
module.exports = {
  'Login Page Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/login')
      .waitForElementVisible('#paper', 5000)
      .assert.elementPresent('.login-container')
      .assert.containsText('.login_title', '系统登录')
      .assert.elementPresent('input[placeholder="账号"]')
      .assert.elementPresent('input[placeholder="密码"]')
      .end()
  },

  'Login Success Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/login')
      .waitForElementVisible('.login-container', 5000)
      .setValue('input[placeholder="账号"]', 'admin')
      .setValue('input[placeholder="密码"]', '123')
      .click('button[type="primary"]')
      .pause(2000)
      // 登录成功后应该跳转到 dashboard
      .assert.urlContains('/admin')
      .end()
  },

  'Login Validation Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/login')
      .waitForElementVisible('.login-container', 5000)
      // 不输入任何内容直接点击登录
      .click('button[type="primary"]')
      .pause(1000)
      // 应该显示验证错误
      .assert.elementPresent('.el-form-item__error')
      .end()
  }
}
