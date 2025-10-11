import { mount, createLocalVue } from '@vue/test-utils'
import Login from '@/components/Login'
import ElementUI from 'element-ui'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import axios from 'axios'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(Vuex)
localVue.use(VueRouter)

jest.mock('axios')

describe('Login.vue', () => {
  let wrapper
  let store
  let router
  let actions

  beforeEach(() => {
    actions = {
      login: jest.fn()
    }

    store = new Vuex.Store({
      state: {
        username: ''
      },
      mutations: {
        login: jest.fn()
      },
      actions
    })

    router = new VueRouter({
      routes: [
        { path: '/login', name: 'Login' },
        { path: '/admin/dashboard', name: 'Dashboard' }
      ]
    })

    axios.post.mockReset()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.destroy()
    }
  })

  it('should render login form', () => {
    wrapper = mount(Login, {
      localVue,
      store,
      router,
      mocks: {
        $axios: axios
      }
    })

    expect(wrapper.find('.login-container').exists()).toBe(true)
    expect(wrapper.find('.login_title').text()).toBe('系统登录')
  })

  it('should validate required fields', async () => {
    wrapper = mount(Login, {
      localVue,
      store,
      router,
      mocks: {
        $axios: axios
      }
    })

    expect(wrapper.vm.rules.username[0].required).toBe(true)
    expect(wrapper.vm.rules.password[0].required).toBe(true)
  })

  it('should handle successful login', async () => {
    const mockResponse = {
      data: {
        code: 200,
        result: { username: 'admin', id: 1 }
      }
    }

    axios.post.mockResolvedValue(mockResponse)

    wrapper = mount(Login, {
      localVue,
      store,
      router,
      mocks: {
        $axios: axios
      }
    })

    wrapper.setData({
      loginForm: {
        username: 'admin',
        password: '123'
      }
    })

    await wrapper.vm.login()
    await wrapper.vm.$nextTick()

    expect(axios.post).toHaveBeenCalledWith('/login', {
      username: 'admin',
      password: '123'
    })
  })

  it('should handle failed login', async () => {
    const mockResponse = {
      data: {
        code: 400,
        message: '用户名或密码错误'
      }
    }

    axios.post.mockResolvedValue(mockResponse)

    // Mock $alert method
    const $alert = jest.fn()

    wrapper = mount(Login, {
      localVue,
      store,
      router,
      mocks: {
        $axios: axios,
        $alert
      }
    })

    wrapper.setData({
      loginForm: {
        username: 'wronguser',
        password: 'wrongpass'
      }
    })

    await wrapper.vm.login()
    await wrapper.vm.$nextTick()

    expect($alert).toHaveBeenCalledWith('用户名或密码错误', '提示', {
      confirmButtonText: '确定'
    })
  })

  it('should have remember password checkbox', () => {
    wrapper = mount(Login, {
      localVue,
      store,
      router,
      mocks: {
        $axios: axios
      }
    })

    expect(wrapper.vm.checked).toBe(true)
    const checkbox = wrapper.find('.login_remember')
    expect(checkbox.exists()).toBe(true)
  })
})
