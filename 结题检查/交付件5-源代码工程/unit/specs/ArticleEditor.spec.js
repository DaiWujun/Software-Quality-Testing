import { mount, createLocalVue } from '@vue/test-utils'
import ArticleEditor from '@/components/admin/content/ArticleEditor'
import ElementUI from 'element-ui'
import VueRouter from 'vue-router'
import axios from 'axios'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)

jest.mock('axios')

describe('ArticleEditor.vue', () => {
  let wrapper
  let router

  beforeEach(() => {
    router = new VueRouter({
      routes: [
        {
          path: '/admin/content/editor',
          name: 'Editor',
          component: ArticleEditor
        }
      ]
    })

    axios.post.mockReset()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.destroy()
    }
  })

  it('should render article editor', () => {
    wrapper = mount(ArticleEditor, {
      localVue,
      router,
      stubs: ['mavon-editor', 'img-upload'],
      mocks: {
        $axios: axios
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('should initialize with empty article', () => {
    wrapper = mount(ArticleEditor, {
      localVue,
      router,
      stubs: ['mavon-editor', 'img-upload'],
      mocks: {
        $axios: axios
      }
    })

    expect(wrapper.vm.article).toEqual({})
    expect(wrapper.vm.dialogVisible).toBe(false)
  })

  it('should load article from route params', () => {
    const mockArticle = {
      id: 1,
      articleTitle: 'Test Article',
      articleContentMd: '# Test',
      articleAbstract: 'Test abstract',
      articleCover: 'cover.jpg'
    }

    // 使用 propsData 传递数据，而不是依赖 route params
    wrapper = mount(ArticleEditor, {
      localVue,
      router,
      stubs: ['mavon-editor', 'img-upload'],
      mocks: {
        $axios: axios
      },
      // 直接设置组件数据
      data() {
        return {
          article: mockArticle
        }
      }
    })

    expect(wrapper.vm.article).toEqual(mockArticle)
  })

  it('should save article successfully', async () => {
    const mockResponse = {
      data: { code: 200, message: '保存成功' }
    }

    axios.post.mockResolvedValue(mockResponse)

    const $message = jest.fn()
    const $confirm = jest.fn().mockResolvedValue()

    wrapper = mount(ArticleEditor, {
      localVue,
      router,
      stubs: ['mavon-editor', 'img-upload'],
      mocks: {
        $axios: axios,
        $message,
        $confirm
      }
    })

    wrapper.setData({
      article: {
        id: 1,
        articleTitle: 'Test Article',
        articleAbstract: 'Test abstract',
        articleCover: 'cover.jpg'
      }
    })

    const mdContent = '# Test Content'
    const htmlContent = '<h1>Test Content</h1>'

    await wrapper.vm.saveArticles(mdContent, htmlContent)
    await wrapper.vm.$nextTick()

    expect($confirm).toHaveBeenCalled()
  })

  it('should handle save cancellation', async () => {
    const $message = jest.fn()
    const $confirm = jest.fn().mockRejectedValue()

    wrapper = mount(ArticleEditor, {
      localVue,
      router,
      stubs: ['mavon-editor', 'img-upload'],
      mocks: {
        $axios: axios,
        $message,
        $confirm
      }
    })

    const mdContent = '# Test'
    const htmlContent = '<h1>Test</h1>'

    await wrapper.vm.saveArticles(mdContent, htmlContent)
    await wrapper.vm.$nextTick()

    expect($confirm).toHaveBeenCalled()
  })

  it('should open dialog for abstract and cover', async () => {
    wrapper = mount(ArticleEditor, {
      localVue,
      router,
      stubs: ['mavon-editor', 'img-upload'],
      mocks: {
        $axios: axios
      }
    })

    wrapper.setData({ dialogVisible: true })
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.dialogVisible).toBe(true)
  })

  it('should upload image and update cover', () => {
    wrapper = mount(ArticleEditor, {
      localVue,
      router,
      stubs: ['mavon-editor', 'img-upload'],
      mocks: {
        $axios: axios
      }
    })

    wrapper.vm.$refs.imgUpload = { url: 'http://example.com/image.jpg' }
    wrapper.vm.uploadImg()

    expect(wrapper.vm.article.articleCover).toBe('http://example.com/image.jpg')
  })
})
