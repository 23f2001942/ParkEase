// frontend/src/router/index.js

import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import UserDashboard from "../views/UserDashboard.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/login", name: "Login", component: Login },
  { path: "/signup", name: "Signup", component: Signup },
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/user/dashboard",
    name: "UserDashboard",
    component: UserDashboard,
    meta: { requiresAuth: true, role: "user" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");
  const role = localStorage.getItem("role");

  if (to.meta.requiresAuth && !token) {
    return next("/login");
  }
  if (to.meta.role && to.meta.role !== role) {
    return next("/");
  }
  next();
});

export default router;
