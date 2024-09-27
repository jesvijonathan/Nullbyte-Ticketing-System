import { createRouter, createWebHistory } from 'vue-router'
import {useAuthStore} from "../stores/auth"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { 
      path: '/',
      redirect: '/login'
    },
    {
      path: '/service',
      name: 'service',
      component: () => import('../views/ServiceDeskView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/logout',
      name: 'logout',
      component: () =>{
        const authStore=useAuthStore()
        authStore.logout();
      },
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      meta: { requiresAuth: false },
      component: () => import('../views/LoginView.vue')
    }
  ]
})

router.beforeEach((to,from,next)=>{
  const authStore=useAuthStore();
  const isAuthenticated=authStore.isAuthenticated;

  if(to.meta.requiresAuth && !isAuthenticated){
    next({name:'login'})
  }
  else{
    next();
  }
})

export default router
