// E2E 测试: 笔记本/文章页面
module.exports = {
  'Jotter Page Load Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/jotter')
      .waitForElementVisible('body', 5000)
      .pause(1000)
      .assert.elementPresent('.el-card')
      .end()
  },

  'Article Details Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/jotter')
      .waitForElementVisible('.el-card', 5000)
      // 点击第一篇文章
      .click('.el-card:first-child')
      .pause(1000)
      // 应该显示文章详情
      .assert.urlContains('/jotter/article')
      .end()
  },

  'Article Pagination Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/jotter')
      .waitForElementVisible('.el-pagination', 5000)
      // 点击下一页
      .click('.el-pagination .btn-next')
      .pause(1000)
      .assert.elementPresent('.el-card')
      .end()
  }
}
