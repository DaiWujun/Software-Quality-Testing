import { mount, createLocalVue } from '@vue/test-utils'
import Tag from '@/components/library/Tag'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('Tag.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Tag, {
      localVue
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.name()).toBe('Tag')
  })

  it('应该渲染5个标签', () => {
    const tags = wrapper.findAllComponents({ name: 'ElTag' })
    expect(tags.length).toBe(5)
  })

  it('应该包含正确的标签名称', () => {
    expect(wrapper.text()).toContain('标签一')
    expect(wrapper.text()).toContain('标签二')
    expect(wrapper.text()).toContain('标签三')
    expect(wrapper.text()).toContain('标签四')
    expect(wrapper.text()).toContain('标签五')
  })

  it('应该为每个标签设置不同的类型', () => {
    const tags = wrapper.vm.tags
    expect(tags[0].type).toBe('')
    expect(tags[1].type).toBe('success')
    expect(tags[2].type).toBe('info')
    expect(tags[3].type).toBe('warning')
    expect(tags[4].type).toBe('danger')
  })

  it('所有标签应该可关闭', () => {
    const tagComponents = wrapper.findAllComponents({ name: 'ElTag' })
    tagComponents.wrappers.forEach(tag => {
      expect(tag.props('closable')).toBe(true)
    })
  })
})
