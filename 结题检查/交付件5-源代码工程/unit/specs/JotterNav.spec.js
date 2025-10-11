import { mount, createLocalVue } from '@vue/test-utils'
import JotterNav from '@/components/jotter/JotterNav'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('JotterNav.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(JotterNav, {
      localVue
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.is(JotterNav)).toBe(true)
  })

  it('应该渲染ElMenu组件', () => {
    const menu = wrapper.findComponent({ name: 'ElMenu' })
    expect(menu.exists()).toBe(true)
  })

  it('ElMenu应该有正确的背景色', () => {
    const menu = wrapper.findComponent({ name: 'ElMenu' })
    expect(menu.props('backgroundColor')).toBe('#545c64')
  })

  it('应该包含ElSubmenu组件', () => {
    const submenu = wrapper.findComponent({ name: 'ElSubmenu' })
    expect(submenu.exists()).toBe(true)
  })

  it('应该包含多个ElMenuItem', () => {
    const menuItems = wrapper.findAllComponents({ name: 'ElMenuItem' })
    expect(menuItems.length).toBeGreaterThan(0)
  })

  it('应该有handleOpen方法', () => {
    expect(typeof wrapper.vm.handleOpen).toBe('function')
  })

  it('应该有handleClose方法', () => {
    expect(typeof wrapper.vm.handleClose).toBe('function')
  })

  it('应该渲染标题"科目"', () => {
    const h4 = wrapper.find('h4')
    expect(h4.exists()).toBe(true)
    expect(h4.text()).toBe('科目')
  })
})
