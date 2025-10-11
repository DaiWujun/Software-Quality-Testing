// E2E 测试: 首页导航
module.exports = {
  'Home Page Load Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer)
      .waitForElementVisible('body', 5000)
      .assert.urlContains('/index')
      .end()
  },

  'Navigation Menu Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer)
      .waitForElementVisible('body', 5000)
      // 检查导航菜单
      .assert.elementPresent('.el-menu')
      .end()
  },

  'Navigate to Library Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer)
      .waitForElementVisible('.el-menu', 5000)
      // 点击图书馆菜单项
      .click('a[href="/library"]')
      .pause(1000)
      .assert.urlContains('/library')
      .end()
  },

  'Navigate to Jotter Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer)
      .waitForElementVisible('.el-menu', 5000)
      // 点击笔记本菜单项
      .click('a[href="/jotter"]')
      .pause(1000)
      .assert.urlContains('/jotter')
      .end()
  }
}
