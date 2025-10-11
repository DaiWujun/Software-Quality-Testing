import { shallowMount, createLocalVue } from '@vue/test-utils'
import Home from '@/components/Home'
import ElementUI from 'element-ui'
import VueRouter from 'vue-router'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)

describe('Home.vue', () => {
  let wrapper
  let router

  beforeEach(() => {
    router = new VueRouter({
      routes: []
    })

    wrapper = shallowMount(Home, {
      localVue,
      router
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.is(Home)).toBe(true)
  })

  it('应该包含NavMenu组件', () => {
    const navMenu = wrapper.findComponent({ name: 'NavMenu' })
    expect(navMenu.exists()).toBe(true)
  })

  it('应该有nav-menu样式类', () => {
    const navMenu = wrapper.find('.nav-menu')
    expect(navMenu.exists()).toBe(true)
  })
})
