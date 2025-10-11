import Vue from 'vue'
import Vuex from 'vuex'
import store from '@/store'

Vue.use(Vuex)

describe('Vuex Store', () => {
  beforeEach(() => {
    // 清空 localStorage 并重置 mock
    window.localStorage.clear()
    window.localStorage.getItem.mockClear()
    window.localStorage.setItem.mockClear()
    window.localStorage.removeItem.mockClear()
  })

  it('should initialize with empty username', () => {
    const state = store.state
    expect(state.username).toBe('')
    expect(state.adminMenus).toEqual([])
  })

  it('should commit login mutation', () => {
    const userData = { username: 'testuser', id: 1 }
    store.commit('login', userData)

    expect(store.state.username).toEqual(userData)
    expect(window.localStorage.setItem).toHaveBeenCalledWith('username', JSON.stringify(userData))
    expect(window.localStorage.getItem('username')).toBe(JSON.stringify(userData))
  })

  it('should commit logout mutation', () => {
    // 先登录
    const userData = { username: 'testuser', id: 1 }
    store.commit('login', userData)

    // 再登出
    store.commit('logout')

    expect(store.state.username).toBe('')
    expect(store.state.adminMenus).toEqual([])
    expect(window.localStorage.removeItem).toHaveBeenCalledWith('username')
    expect(window.localStorage.getItem('username')).toBeNull()
  })

  it('should initialize admin menus', () => {
    const menus = [
      { path: '/admin/dashboard', name: 'Dashboard' },
      { path: '/admin/content', name: 'Content' }
    ]

    store.commit('initAdminMenu', menus)
    expect(store.state.adminMenus).toEqual(menus)
  })

  it('should restore username from localStorage', () => {
    const userData = { username: 'testuser', id: 1 }
    window.localStorage.setItem('username', JSON.stringify(userData))

    // 重新创建 store 实例模拟页面刷新
    const newStore = new Vuex.Store({
      state: {
        username: window.localStorage.getItem('username') == null ? '' : JSON.parse(window.localStorage.getItem('username' || '[]')),
        adminMenus: []
      }
    })

    expect(newStore.state.username).toEqual(userData)
  })
})
