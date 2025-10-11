import { mount, createLocalVue } from '@vue/test-utils'
import QuickNav from '@/components/home/QuickNav'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('QuickNav.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(QuickNav, {
      localVue
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.is(QuickNav)).toBe(true)
  })

  it('应该有quick-nav样式类', () => {
    const quickNav = wrapper.find('.quick-nav')
    expect(quickNav.exists()).toBe(true)
  })

  it('应该包含4张图片', () => {
    const images = wrapper.findAll('img')
    expect(images.length).toBe(4)
  })

  it('应该包含monster图片', () => {
    const monster = wrapper.find('.monster')
    expect(monster.exists()).toBe(true)
  })

  it('应该包含readme图片', () => {
    const readme = wrapper.find('.readme')
    expect(readme.exists()).toBe(true)
  })

  it('应该包含logo图片', () => {
    const logo = wrapper.find('.logo')
    expect(logo.exists()).toBe(true)
  })

  it('应该包含GitHub README链接', () => {
    const link = wrapper.find('a')
    expect(link.exists()).toBe(true)
    expect(link.attributes('href')).toContain('github.com')
  })
})
