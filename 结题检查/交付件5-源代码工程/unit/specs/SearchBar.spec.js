import { mount, createLocalVue } from '@vue/test-utils'
import SearchBar from '@/components/library/SearchBar'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('SearchBar.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(SearchBar, {
      localVue
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.name()).toBe('SearchBar')
  })

  it('应该渲染搜索输入框', () => {
    const input = wrapper.findComponent({ name: 'ElInput' })
    expect(input.exists()).toBe(true)
    // Element UI的Input组件实际prop名称可能不同
    const inputElement = wrapper.find('input')
    expect(inputElement.exists()).toBe(true)
    expect(inputElement.attributes('placeholder')).toBe('通过书名或作者搜索...')
  })

  it('应该渲染搜索按钮', () => {
    const button = wrapper.findComponent({ name: 'ElButton' })
    expect(button.exists()).toBe(true)
    expect(button.text()).toContain('搜索')
  })

  it('应该双向绑定 keywords', async () => {
    const input = wrapper.findComponent({ name: 'ElInput' })
    await input.vm.$emit('input', '测试关键词')
    expect(wrapper.vm.keywords).toBe('测试关键词')
  })

  it('点击搜索按钮应该触发 onSearch 事件', async () => {
    const button = wrapper.find('button')
    await button.trigger('click')
    expect(wrapper.emitted('onSearch')).toBeTruthy()
    expect(wrapper.emitted('onSearch').length).toBe(1)
  })

  it('按 Enter 键应该触发 onSearch 事件', async () => {
    const input = wrapper.find('input')
    await input.trigger('keyup.enter')
    expect(wrapper.emitted('onSearch')).toBeTruthy()
  })

  it('应该有正确的初始数据', () => {
    expect(wrapper.vm.keywords).toBe('')
    expect(wrapper.vm.books).toEqual([])
    expect(wrapper.vm.cardLoading).toEqual([])
  })
})
