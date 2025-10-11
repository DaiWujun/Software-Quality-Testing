import { mount, createLocalVue } from '@vue/test-utils'
import Articles from '@/components/jotter/Articles'
import ElementUI from 'element-ui'
import VueRouter from 'vue-router'
import axios from 'axios'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
jest.mock('axios')

describe('Articles.vue', () => {
  let wrapper
  let router

  beforeEach(() => {
    axios.get.mockReset()
    axios.get.mockResolvedValue({
      data: {
        code: 200,
        result: {
          content: [],
          totalElements: 0
        }
      }
    })

    router = new VueRouter({
      routes: [
        { path: '/jotter/article', name: 'article' }
      ]
    })

    wrapper = mount(Articles, {
      localVue,
      router,
      mocks: {
        $axios: axios
      }
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('应该正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.is(Articles)).toBe(true)
  })

  it('应该有articles数据数组', () => {
    expect(wrapper.vm.articles).toBeDefined()
    expect(Array.isArray(wrapper.vm.articles)).toBe(true)
  })

  it('应该有pageSize和total数据', () => {
    expect(wrapper.vm.pageSize).toBe(4)
    expect(wrapper.vm.total).toBe(0)
  })

  it('mounted时应该调用loadArticles', () => {
    expect(axios.get).toHaveBeenCalledWith('/article/4/1')
  })

  it('loadArticles应该加载文章列表', async () => {
    const mockArticles = [
      { id: 1, articleTitle: '测试文章1', articleDate: '2025-01-01', articleAbstract: '摘要1' },
      { id: 2, articleTitle: '测试文章2', articleDate: '2025-01-02', articleAbstract: '摘要2' }
    ]

    axios.get.mockResolvedValueOnce({
      data: {
        code: 200,
        result: {
          content: mockArticles,
          totalElements: 10
        }
      }
    })

    await wrapper.vm.loadArticles()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.articles).toEqual(mockArticles)
    expect(wrapper.vm.total).toBe(10)
  })

  it('handleCurrentChange应该加载指定页的文章', async () => {
    const mockArticles = [
      { id: 3, articleTitle: '第2页文章', articleDate: '2025-01-03', articleAbstract: '第2页' }
    ]

    axios.get.mockResolvedValueOnce({
      data: {
        code: 200,
        result: {
          content: mockArticles,
          totalElements: 10
        }
      }
    })

    await wrapper.vm.handleCurrentChange(2)
    await wrapper.vm.$nextTick()

    expect(axios.get).toHaveBeenCalledWith('/article/4/2')
    expect(wrapper.vm.articles).toEqual(mockArticles)
  })

  it('应该渲染ElCard组件', () => {
    const card = wrapper.findComponent({ name: 'ElCard' })
    expect(card.exists()).toBe(true)
  })

  it('应该渲染分页组件', () => {
    const pagination = wrapper.findComponent({ name: 'ElPagination' })
    expect(pagination.exists()).toBe(true)
  })

  it('分页组件应该有正确的props', () => {
    const pagination = wrapper.findComponent({ name: 'ElPagination' })
    expect(pagination.props('pageSize')).toBe(4)
    expect(pagination.props('total')).toBe(0)
  })
})
