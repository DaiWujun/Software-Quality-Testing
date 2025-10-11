import { mount, createLocalVue } from '@vue/test-utils'
import Books from '@/components/library/Books'
import ElementUI from 'element-ui'
import axios from 'axios'

const localVue = createLocalVue()
localVue.use(ElementUI)

// Mock axios
jest.mock('axios')

describe('Books.vue', () => {
  let wrapper

  beforeEach(() => {
    // 重置 mock 并设置默认返回值
    axios.get.mockReset()
    axios.get.mockResolvedValue({
      data: { code: 200, result: [] }
    })
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.destroy()
    }
  })

  it('should render books component', async () => {
    wrapper = mount(Books, {
      localVue,
      stubs: ['search-bar', 'view-switch'],
      mocks: {
        $axios: axios
      }
    })

    await wrapper.vm.$nextTick()
    expect(wrapper.exists()).toBe(true)
  })

  it('should load books on mount', async () => {
    const mockBooks = [
      { id: 1, title: 'Test Book 1', author: 'Author 1', cover: 'cover1.jpg' },
      { id: 2, title: 'Test Book 2', author: 'Author 2', cover: 'cover2.jpg' }
    ]

    axios.get.mockResolvedValue({
      data: { code: 200, result: mockBooks }
    })

    wrapper = mount(Books, {
      localVue,
      stubs: ['search-bar', 'view-switch'],
      mocks: {
        $axios: axios
      }
    })

    await wrapper.vm.$nextTick()

    expect(axios.get).toHaveBeenCalledWith('/books')
    expect(wrapper.vm.books).toEqual(mockBooks)
  })

  it('should handle page change', async () => {
    wrapper = mount(Books, {
      localVue,
      stubs: ['search-bar', 'view-switch'],
      mocks: {
        $axios: axios
      }
    })

    await wrapper.vm.$nextTick()
    wrapper.vm.handleCurrentChange(2)
    expect(wrapper.vm.currentPage).toBe(2)
  })

  it('should search books with keywords', async () => {
    const mockSearchResults = [
      { id: 3, title: 'Search Result', author: 'Author 3', cover: 'cover3.jpg' }
    ]

    axios.get.mockResolvedValue({
      data: { code: 200, result: mockSearchResults }
    })

    wrapper = mount(Books, {
      localVue,
      stubs: ['search-bar', 'view-switch'],
      mocks: {
        $axios: axios
      }
    })

    // 模拟 searchBar ref
    wrapper.vm.$refs.searchBar = { keywords: 'test' }
    await wrapper.vm.searchResult()
    await wrapper.vm.$nextTick()

    expect(axios.get).toHaveBeenCalledWith('/search?keywords=test', {})
    expect(wrapper.vm.books).toEqual(mockSearchResults)
  })

  it('should paginate books correctly', async () => {
    const mockBooks = Array.from({ length: 30 }, (_, i) => ({
      id: i + 1,
      title: `Book ${i + 1}`,
      author: `Author ${i + 1}`,
      cover: `cover${i + 1}.jpg`
    }))

    wrapper = mount(Books, {
      localVue,
      stubs: ['search-bar', 'view-switch'],
      mocks: {
        $axios: axios
      }
    })

    await wrapper.vm.$nextTick()
    wrapper.setData({ books: mockBooks, currentPage: 1, pagesize: 18 })

    // 第一页应该显示 18 本书
    const firstPageBooks = wrapper.vm.books.slice(0, 18)
    expect(firstPageBooks.length).toBe(18)

    // 切换到第二页
    wrapper.vm.handleCurrentChange(2)
    const secondPageBooks = wrapper.vm.books.slice(18, 36)
    expect(secondPageBooks.length).toBe(12)
  })
})
