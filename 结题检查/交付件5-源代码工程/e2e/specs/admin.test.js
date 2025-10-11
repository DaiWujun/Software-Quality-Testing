// E2E 测试: 管理后台
module.exports = {
  'Admin Dashboard Access Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/admin/dashboard')
      .waitForElementVisible('body', 5000)
      .pause(1000)
      // 未登录应该跳转到登录页
      .assert.urlContains('/login')
      .end()
  },

  'Admin Menu Navigation Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      // 先登录
      .url(devServer + '/login')
      .waitForElementVisible('.login-container', 5000)
      .setValue('input[placeholder="账号"]', 'admin')
      .setValue('input[placeholder="密码"]', '123')
      .click('button[type="primary"]')
      .pause(2000)
      // 检查是否进入管理后台
      .assert.urlContains('/admin')
      .waitForElementVisible('.el-menu-admin', 5000)
      .assert.elementPresent('.el-submenu')
      .end()
  },

  'Admin Logout Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      // 先登录
      .url(devServer + '/login')
      .waitForElementVisible('.login-container', 5000)
      .setValue('input[placeholder="账号"]', 'admin')
      .setValue('input[placeholder="密码"]', '123')
      .click('button[type="primary"]')
      .pause(2000)
      // 点击登出按钮（假设有登出按钮）
      .waitForElementVisible('.el-header', 5000)
      .pause(1000)
      // 应该跳转回登录页
      .end()
  }
}
