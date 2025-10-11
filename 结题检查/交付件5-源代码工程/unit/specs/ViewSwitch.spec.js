import { mount, createLocalVue } from '@vue/test-utils'
import ViewSwitch from '@/components/library/ViewSwitch'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('ViewSwitch.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(ViewSwitch, {
      localVue
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.is(ViewSwitch)).toBe(true)
  })

  it('应该渲染ElSwitch组件', () => {
    const switchComponent = wrapper.findComponent({ name: 'ElSwitch' })
    expect(switchComponent.exists()).toBe(true)
  })

  it('应该有value数据属性', () => {
    expect(wrapper.vm.value).toBeDefined()
    expect(typeof wrapper.vm.value).toBe('boolean')
  })

  it('value默认应该为true', () => {
    expect(wrapper.vm.value).toBe(true)
  })

  it('应该能切换value的值', async () => {
    expect(wrapper.vm.value).toBe(true)
    wrapper.vm.value = false
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.value).toBe(false)
  })
})
