import { mount, createLocalVue } from '@vue/test-utils'
import NavMenu from '@/components/common/NavMenu'
import ElementUI from 'element-ui'
import VueRouter from 'vue-router'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)

describe('NavMenu.vue', () => {
  let wrapper
  let router

  beforeEach(() => {
    router = new VueRouter({
      routes: [
        { path: '/', name: 'index' },
        { path: '/index', name: 'index' },
        { path: '/jotter', name: 'jotter' },
        { path: '/library', name: 'library' },
        { path: '/login', name: 'login' }
      ]
    })

    wrapper = mount(NavMenu, {
      localVue,
      router
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.is(NavMenu)).toBe(true)
  })

  it('应该渲染导航菜单', () => {
    const menu = wrapper.findComponent({ name: 'ElMenu' })
    expect(menu.exists()).toBe(true)
  })

  it('应该包含4个菜单项', () => {
    const menuItems = wrapper.findAllComponents({ name: 'ElMenuItem' })
    expect(menuItems.length).toBe(4)
  })

  it('应该有navList数据', () => {
    expect(wrapper.vm.navList).toBeDefined()
    expect(Array.isArray(wrapper.vm.navList)).toBe(true)
    expect(wrapper.vm.navList.length).toBe(4)
  })

  it('应该包含搜索输入框', () => {
    const input = wrapper.findComponent({ name: 'ElInput' })
    expect(input.exists()).toBe(true)
  })

  it('应该有keywords数据属性', () => {
    expect(wrapper.vm.keywords).toBeDefined()
    expect(wrapper.vm.keywords).toBe('')
  })

  it('应该有currentPath计算属性', () => {
    expect(wrapper.vm.currentPath).toBeDefined()
  })
})
