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
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
  },
  {
    path: '/chat-about-yan',
    name: 'chat-about-yan',
    component: () => import('@/views/ChatMeView.vue'),
  },
  {
    path: '/chat-doc',
    name: 'chat-doc',
    component: () => import('@/views/ChatDocView.vue'),
  },
  {
    path: '/llm-admin',
    name: 'llm-admin',
    component: () => import('@/views/LLMAdminView.vue'),
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
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

export default router;
