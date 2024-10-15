import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from "../stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/dashboard',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: {
        breadcrumb: [{ name: 'Dashboard', path: '/dashboard' }]
      },
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore();
        const isAuthenticated = authStore.isAuthenticated;
        if (!isAuthenticated) {
          next('/login');
        } else {
          next();
        }
      }
    },
    {
      path: '/create_ticket',
      name: 'create_ticket',
      component: () => import('../views/CreateTicket.vue'),

    },
    {
      path: '/list_tickets',
      name: 'list_tickets',
      component: () => import('../views/ViewTickets.vue'),

    }, {
      path: '/tickets',
      name: 'tickets',
      component: () => import('../views/TicketMenu.vue'),

    },
    {
      path: '/ticket/:id?',
      name: 'ticket',
      component: () => import('../views/Ticket.vue'),
      props: route => ({ id: route.params.id || route.query.id }),
        },
    {
      path: '/service',
      name: 'service',
      component: () => import('../views/ServiceDeskView.vue'),
      meta: {
        breadcrumb: [{ name: 'Dashboard', path: '/dashboard' }, { name: 'Service', path: '/service' }],
        requiresAuth: true
      }
    },
    {
      path: '/complaint',
      name: 'complaint',
      component: () => import('../views/Complaint.vue'),
      meta: {
        breadcrumb: [{ name: 'Dashboard', path: '/dashboard' }, { name: 'Complaint', path: '/complaint' }],
        requiresAuth: true
      }
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => {
        const authStore = useAuthStore();
        authStore.logout();
      },
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresAuth: false }
    }
  ]
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;
