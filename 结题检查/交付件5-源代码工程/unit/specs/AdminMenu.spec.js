import { mount, createLocalVue } from '@vue/test-utils'
import AdminMenu from '@/components/admin/AdminMenu'
import ElementUI from 'element-ui'
import Vuex from 'vuex'
import VueRouter from 'vue-router'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(Vuex)
localVue.use(VueRouter)

describe('AdminMenu.vue', () => {
  let wrapper
  let store
  let router

  beforeEach(() => {
    const mockMenus = [
      {
        path: '/admin/dashboard',
        name: 'Dashboard',
        nameZh: '仪表盘',
        iconCls: 'el-icon-s-home',
        children: []
      },
      {
        path: '/admin/content',
        name: 'Content',
        nameZh: '内容管理',
        iconCls: 'el-icon-document',
        children: [
          {
            path: '/admin/content/book',
            name: 'BookManagement',
            nameZh: '图书管理',
            icon: 'el-icon-reading'
          },
          {
            path: '/admin/content/article',
            name: 'ArticleManagement',
            nameZh: '文章管理',
            icon: 'el-icon-edit'
          }
        ]
      }
    ]

    store = new Vuex.Store({
      state: {
        adminMenus: mockMenus
      }
    })

    router = new VueRouter({
      routes: [
        { path: '/admin/dashboard', name: 'Dashboard' },
        { path: '/admin/content/book', name: 'BookManagement' },
        { path: '/admin/content/article', name: 'ArticleManagement' }
      ]
    })
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.destroy()
    }
  })

  it('should render admin menu', () => {
    wrapper = mount(AdminMenu, {
      localVue,
      store,
      router
    })

    expect(wrapper.find('.el-menu-admin').exists()).toBe(true)
  })

  it('should display correct menu items', () => {
    wrapper = mount(AdminMenu, {
      localVue,
      store,
      router
    })

    const adminMenus = wrapper.vm.adminMenus
    expect(adminMenus.length).toBe(2)
    expect(adminMenus[0].nameZh).toBe('仪表盘')
    expect(adminMenus[1].nameZh).toBe('内容管理')
    expect(adminMenus[1].children.length).toBe(2)
  })

  it('should highlight current route', () => {
    router.push('/admin/dashboard')

    wrapper = mount(AdminMenu, {
      localVue,
      store,
      router
    })

    expect(wrapper.vm.currentPath).toBe('/admin/dashboard')
  })

  it('should render submenu items correctly', () => {
    wrapper = mount(AdminMenu, {
      localVue,
      store,
      router
    })

    const submenus = wrapper.findAll('.el-submenu')
    expect(submenus.length).toBeGreaterThan(0)
  })

  it('should not collapse by default', () => {
    wrapper = mount(AdminMenu, {
      localVue,
      store,
      router
    })

    expect(wrapper.vm.isCollapse).toBe(false)
  })
})
