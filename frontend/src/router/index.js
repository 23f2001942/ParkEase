// frontend/src/router/index.js

import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
import UserDashboard from "../views/UserDashboard.vue";

import AdminLayout from "../components/AdminLayout.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import UsersView from "../views/UsersView.vue";
import SearchView from "../views/SearchView.vue";
import SummaryView from "../views/SummaryView.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/login", name: "Login", component: Login },
  { path: "/signup", name: "Signup", component: Signup },

  {
    path: "/admin",
    component: AdminLayout,
    meta: { requiresAuth: true, role: "admin", layout: "admin" },
    children: [
      {
        path: "dashboard",
        name: "AdminDashboard",
        component: AdminDashboard,
      },
      {
        path: "users",
        name: "Users",
        component: UsersView,
      },
      {
        path: "search",
        name: "Search",
        component: SearchView,
      },
      {
        path: "summary",
        name: "Summary",
        component: SummaryView,
      },
      // default to /admin/dashboard
      { path: "", redirect: { name: "AdminDashboard" } },
    ],
  },

  {
    path: "/user/dashboard",
    name: "UserDashboard",
    component: UserDashboard,
    meta: { requiresAuth: true, role: "user" },
  },

  // catch-all
  { path: "/:pathMatch(.*)*", redirect: "/" },
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
