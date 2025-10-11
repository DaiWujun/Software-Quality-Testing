import { mount, createLocalVue } from '@vue/test-utils'
import Register from '@/components/Register'
import ElementUI from 'element-ui'
import axios from 'axios'

const localVue = createLocalVue()
localVue.use(ElementUI)
jest.mock('axios')

describe('Register.vue', () => {
  let wrapper

  beforeEach(() => {
    axios.post = jest.fn().mockResolvedValue({
      data: { code: 200, message: '注册成功' }
    })

    wrapper = mount(Register, {
      localVue,
      mocks: {
        $axios: axios,
        $router: {
          replace: jest.fn()
        },
        $alert: jest.fn()
      }
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('h3').text()).toBe('用户注册')
  })

  it('应该有5个输入框', () => {
    const inputs = wrapper.findAllComponents({ name: 'ElInput' })
    expect(inputs.length).toBe(5)
  })

  it('应该渲染注册按钮', () => {
    const button = wrapper.findComponent({ name: 'ElButton' })
    expect(button.exists()).toBe(true)
    expect(button.text()).toContain('注册')
  })

  it('应该有正确的初始数据', () => {
    expect(wrapper.vm.loginForm).toEqual({
      username: '',
      password: '',
      name: '',
      phone: '',
      email: ''
    })
    expect(wrapper.vm.loading).toBe(false)
    expect(wrapper.vm.checked).toBe(true)
  })

  it('应该有表单验证规则', () => {
    expect(wrapper.vm.rules.username).toBeDefined()
    expect(wrapper.vm.rules.password).toBeDefined()
    expect(wrapper.vm.rules.username[0].required).toBe(true)
    expect(wrapper.vm.rules.password[0].required).toBe(true)
  })

  it('应该绑定用户名输入框', async () => {
    const usernameInput = wrapper.findAll('input').at(0)
    await usernameInput.setValue('testuser')
    expect(wrapper.vm.loginForm.username).toBe('testuser')
  })

  it('应该绑定密码输入框', async () => {
    const passwordInput = wrapper.findAll('input').at(1)
    await passwordInput.setValue('testpass')
    expect(wrapper.vm.loginForm.password).toBe('testpass')
  })

  it('提交注册时应该调用 API', async () => {
    wrapper.vm.loginForm = {
      username: 'newuser',
      password: 'password123',
      name: '测试用户',
      phone: '13800138000',
      email: 'test@example.com'
    }

    await wrapper.vm.register()

    expect(axios.post).toHaveBeenCalledWith('/register', {
      username: 'newuser',
      password: 'password123',
      name: '测试用户',
      phone: '13800138000',
      email: 'test@example.com'
    })
  })

  it('注册成功应该跳转到登录页', async () => {
    axios.post.mockResolvedValue({
      data: { code: 200, message: '注册成功' }
    })

    await wrapper.vm.register()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.$router.replace).toHaveBeenCalledWith('/login')
  })

  it('注册失败应该显示错误信息', async () => {
    axios.post.mockResolvedValue({
      data: { code: 400, message: '用户名已存在' }
    })

    await wrapper.vm.register()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.$alert).toHaveBeenCalledWith('用户名已存在', '提示', {
      confirmButtonText: '确定'
    })
  })
})
