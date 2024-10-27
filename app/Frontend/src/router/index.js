import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from "../stores/auth";

let move_to_login = true; // Set this to false to skip automatic redirection to login

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
        if (true) {
          next('/about');
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
    },
    {
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
      path: '/chatbot',
      name: 'chatbot',
      component: () => import('../views/ChatboMenu.vue'),
      meta: {
        breadcrumb: [{ name: 'Dashboard', path: '/dashboard' }, { name: 'Complaint', path: '/complaint' }],
        requiresAuth: true
      }
    },
    {
      path: '/vertex',
      name: 'Chatbot Vertex',
      component: () => import('../views/Chatbot.vue'),
      meta: {
        breadcrumb: [{ name: 'Dashboard', path: '/dashboard' }, { name: 'Complaint', path: '/complaint' }],
        requiresAuth: true
      }
    },
    {
      path: '/llama',
      name: 'Chatbot Llama',
      component: () => import('../views/Chatbot.vue'),
      meta: {
        breadcrumb: [{ name: 'Dashboard', path: '/dashboard' }, { name: 'Complaint', path: '/complaint' }],
        requiresAuth: true
      }
    },
    {
      path: '/inbox',
      name: 'Inbox',
      component: () => import('../views/Inbox.vue'),
      meta: {
        breadcrumb: [{ name: 'Dashboard', path: '/dashboard' }, { name: 'Complaint', path: '/complaint' }],
        requiresAuth: true
      }
    },
    {
      path: '/about',
      name: 'About',
      component: () => import('../views/About.vue'),
      meta: {
        breadcrumb: [{ name: 'Dashboard', path: '/dashboard' }, { name: 'Complaint', path: '/complaint' }],
        requiresAuth: true
      }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/Profile.vue'),
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
        
        // Perform logout from auth store
        authStore.logout();
    
        // Delete 'user' and 'session' cookies
        document.cookie = "user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    
        // Optionally, you can also redirect after logout
        window.location.href = '/login';
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

  // Check for requiresAuth and move_to_login flag
  if (to.meta.requiresAuth && !isAuthenticated && move_to_login) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;
