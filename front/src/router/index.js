import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: () => import('../pages/Main.vue'),
    redirect: {name: 'page1'},
    name: 'main',
    children: [
      {
        path: '/page1',
        component: () => import('../pages/Main/Page1.vue'),
        name: 'page1',
        meta: { theme: '#55884F' }
      },
      {
        path: '/page2',
        component: () => import('../pages/Main/Page2.vue'),
        name: 'page2',
        meta: { theme: '#544F88' }
      },  
      {
        path: '/page3',
        component: () => import('../pages/Main/Page3.vue'),
        name: 'page3',
        meta: { theme: '#37889A' }
      },  
      {
        path: '/page4',
        component: () => import('../pages/Main/Page4.vue'),
        name: 'page4',
        meta: { theme: '#374D9A' }
      }  
    ]
  },
]

const router = new VueRouter({
  routes
})

export default router
