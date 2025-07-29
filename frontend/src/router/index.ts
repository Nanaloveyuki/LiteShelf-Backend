import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import BookShelf from '../views/BookShelf.vue';
import Discovery from '../views/Discovery.vue';
import Settings from '../views/Settings.vue';

/**
 * 路由配置文件
 * Router configuration file
 */

const routes: Array<RouteRecordRaw> = [
  { path: '/', redirect: '/books' },
  { path: '/books', name: 'BookShelf', component: BookShelf },
  { path: '/discover', name: 'Discovery', component: Discovery },
  { path: '/settings', name: 'Settings', component: Settings }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;