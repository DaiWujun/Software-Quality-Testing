// E2E 测试: 图书馆页面
module.exports = {
  'Library Page Load Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/library')
      .waitForElementVisible('.el-card', 5000)
      .assert.elementPresent('.book')
      .assert.elementPresent('.el-pagination')
      .end()
  },

  'Book Search Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/library')
      .waitForElementVisible('.el-card', 5000)
      // 假设有搜索输入框
      .setValue('input[type="text"]', 'Vue')
      .pause(1000)
      // 应该显示搜索结果
      .assert.elementPresent('.book')
      .end()
  },

  'Book Pagination Test': function (browser) {
    const devServer = browser.globals.devServerURL

    browser
      .url(devServer + '/library')
      .waitForElementVisible('.el-pagination', 5000)
      // 点击第二页
      .click('.el-pagination .el-pager li:nth-child(2)')
      .pause(1000)
      .assert.elementPresent('.book')
      .end()
  }
}
