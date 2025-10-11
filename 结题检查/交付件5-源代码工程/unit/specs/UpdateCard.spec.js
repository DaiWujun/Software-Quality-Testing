import { mount, createLocalVue } from '@vue/test-utils'
import UpdateCard from '@/components/home/UpdateCard'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('UpdateCard.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(UpdateCard, {
      localVue
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.is(UpdateCard)).toBe(true)
  })

  it('应该渲染ElCard组件', () => {
    const card = wrapper.findComponent({ name: 'ElCard' })
    expect(card.exists()).toBe(true)
  })

  it('应该包含"最近更新"标题', () => {
    const text = wrapper.text()
    expect(text).toContain('最近更新')
  })

  it('应该渲染ElTimeline组件', () => {
    const timeline = wrapper.findComponent({ name: 'ElTimeline' })
    expect(timeline.exists()).toBe(true)
  })

  it('应该包含5个时间线项目', () => {
    const timelineItems = wrapper.findAllComponents({ name: 'ElTimelineItem' })
    expect(timelineItems.length).toBe(5)
  })

  it('应该包含更新内容', () => {
    const text = wrapper.text()
    expect(text).toContain('实现上传至服务器和输入 URL 两种方式添加封面')
    expect(text).toContain('实现图书分类功能')
    expect(text).toContain('实现图书分页')
    expect(text).toContain('实现搜索框模糊查询')
    expect(text).toContain('实现图书修改功能')
  })

  it('应该包含时间戳', () => {
    const text = wrapper.text()
    expect(text).toContain('2019/4/13')
    expect(text).toContain('2019/4/11')
    expect(text).toContain('2019/4/8')
  })

  it('应该包含提交者信息', () => {
    const text = wrapper.text()
    expect(text).toContain('Evan 提交于')
  })
})
