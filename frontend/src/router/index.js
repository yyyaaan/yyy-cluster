import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
  },
  {
    path: '/bot/chat',
    redirect: { name: 'chat-about-yan' },
  },
  {
    path: '/toolbox',
    name: 'toolbox',
    component: () => import('@/views/ToolboxView.vue'),
  },
  {
    path: '/chat-about-yan',
    name: 'chat-about-yan',
    component: () => import('@/views/ChatMeView.vue'),
  },
  {
    path: '/chat-codebase',
    name: 'codebase',
    component: () => import('@/views/ChatCodebaseView.vue'),
    meta: { requireAuth: true },
  },
  {
    path: '/chat-log',
    name: 'chat-log',
    component: () => import('@/views/ChatLogView.vue'),
    meta: { requireAdmin: true },
  },
  {
    path: '/chat-doc',
    name: 'chat-doc',
    component: () => import('@/views/ChatDocView.vue'),
    meta: { requireAuth: true },
  },
  {
    path: '/code-bot',
    name: 'code-bot',
    component: () => import('@/views/CodeBotView.vue'),
    meta: { requireAuth: true },
  },
  {
    path: '/llm-admin',
    name: 'llm-admin',
    component: () => import('@/views/LLMAdminView.vue'),
    meta: { requireAdmin: true },
  },
  {
    path: '/llm-design',
    name: 'llm-design',
    component: () => import('@/views/LLMDesignView.vue'),
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requireAuth: true },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginRequiredView.vue'),
  },
  {
    path: '/vue-auth-callback',
    name: 'auth-callback',
    component: () => import('@/views/LoginCallbackView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const jwt = window.localStorage.getItem('jwt');
  if ((!to.meta.requireAuth) && (!to.meta.requireAdmin)) {
    next();
    return;
  }
  if (!jwt) {
    next('/login');
    return;
  }
  const jwtAge = (new Date()) - Date.parse(window.localStorage.getItem('renewedOn'));
  if (jwtAge > 8.6e+7) {
    next('/login');
    return; // expired token
  }

  if (!to.meta.requireAdmin) {
    next();
    return;
  }
  // only admin required goes here
  const response = await fetch(
    `${window.apiRoot}/bot/admin`,
    { method: 'GET', headers: { Authorization: `Bearer ${jwt}` } },
  );
  if (response.ok) {
    next();
  } else {
    next({ name: 'login', query: { adminRequired: 1 } });
  }
});

export default router;
