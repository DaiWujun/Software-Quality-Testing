import { mount, createLocalVue } from '@vue/test-utils'
import Slogan from '@/components/home/Slogan'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('Slogan.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Slogan, {
      localVue
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.is(Slogan)).toBe(true)
  })

  it('应该渲染ElCard组件', () => {
    const card = wrapper.findComponent({ name: 'ElCard' })
    expect(card.exists()).toBe(true)
  })

  it('应该包含Slogan文本', () => {
    const text = wrapper.text()
    expect(text).toContain('Talk is nothing, show you my code.')
  })

  it('应该包含GitHub链接', () => {
    const links = wrapper.findAll('a')
    expect(links.length).toBeGreaterThanOrEqual(1)
    const githubLink = links.filter(link => link.attributes('href').includes('github')).at(0)
    expect(githubLink.exists()).toBe(true)
  })

  it('应该包含CSDN链接', () => {
    const links = wrapper.findAll('a')
    const csdnLink = links.filter(link => link.attributes('href').includes('csdn')).at(0)
    expect(csdnLink.exists()).toBe(true)
  })
})
