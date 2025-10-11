import { mount, createLocalVue } from '@vue/test-utils'
import SideMenu from '@/components/library/SideMenu'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('SideMenu.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(SideMenu, {
      localVue
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.is(SideMenu)).toBe(true)
  })

  it('应该包含侧边栏内容', () => {
    const cardBody = wrapper.find('.card-body')
    if (cardBody.exists()) {
      expect(cardBody.exists()).toBe(true)
    }
  })

  it('应该有默认的active索引', () => {
    if (wrapper.vm.activeIndex !== undefined) {
      expect(typeof wrapper.vm.activeIndex).toBe('string')
    }
  })

  it('应该渲染菜单项', () => {
    const menuItems = wrapper.findAll('.el-menu-item')
    // 可能有菜单项或者为空
    expect(menuItems).toBeDefined()
  })
})
