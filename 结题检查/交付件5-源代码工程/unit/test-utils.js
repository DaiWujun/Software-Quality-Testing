// 测试工具函数
import { createLocalVue } from '@vue/test-utils'
import ElementUI from 'element-ui'
import Vuex from 'vuex'
import VueRouter from 'vue-router'

/**
 * 创建配置好的 localVue 实例
 */
export function createTestVue() {
  const localVue = createLocalVue()
  localVue.use(ElementUI)
  localVue.use(Vuex)
  localVue.use(VueRouter)
  return localVue
}

/**
 * 创建 mock axios 实例
 */
export function createMockAxios() {
  return {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn()
  }
}

/**
 * 创建 mock store
 */
export function createMockStore(state = {}) {
  return new Vuex.Store({
    state: {
      username: '',
      adminMenus: [],
      ...state
    },
    mutations: {
      login: jest.fn(),
      logout: jest.fn(),
      initAdminMenu: jest.fn()
    }
  })
}

/**
 * 创建 mock router
 */
export function createMockRouter(routes = []) {
  return new VueRouter({
    mode: 'history',
    routes: [
      { path: '/login', name: 'Login' },
      { path: '/admin/dashboard', name: 'Dashboard' },
      ...routes
    ]
  })
}

/**
 * 等待异步更新完成
 */
export function flushPromises() {
  return new Promise(resolve => setImmediate(resolve))
}

/**
 * Mock Element UI 消息提示
 */
export function createMockMessage() {
  return {
    success: jest.fn(),
    warning: jest.fn(),
    info: jest.fn(),
    error: jest.fn()
  }
}

/**
 * Mock Element UI 确认框
 */
export function createMockConfirm(willResolve = true) {
  return jest.fn(() =>
    willResolve ? Promise.resolve() : Promise.reject()
  )
}

/**
 * Mock Element UI 提示框
 */
export function createMockAlert() {
  return jest.fn()
}

/**
 * 模拟 API 响应
 */
export function mockApiResponse(data, code = 200) {
  return {
    data: {
      code,
      result: data,
      message: code === 200 ? 'success' : 'error'
    }
  }
}

/**
 * 模拟失败的 API 响应
 */
export function mockApiError(message = 'Error', code = 400) {
  return {
    data: {
      code,
      message
    }
  }
}
