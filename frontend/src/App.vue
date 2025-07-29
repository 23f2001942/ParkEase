<!-- frontend/src/App.vue -->

<template>
  <div>
    <!-- PUBLIC NAVBAR: only when not in an admin and user route -->
    <nav v-if="!isAdminRoute" class="main-nav">
      <div class="nav-left">Welcome to ParkEase</div>
      <div class="nav-center">
        <router-link to="/">Home</router-link>
      </div>
      <div class="nav-right">
        <template v-if="!isAuth">
          <router-link to="/login">Login</router-link> |
          <router-link to="/signup">Sign Up</router-link>
        </template>
        <template v-else>
          <router-link :to="dashboardPath">Dashboard</router-link> |
          <a href="#" @click.prevent="logout">Logout</a>
        </template>
      </div>
    </nav>

    <!-- render either public pages or AdminLayout -->
    <router-view />
  </div>
</template>

<script setup>
import { inject, computed } from "vue";
import { useRouter, useRoute } from "vue-router";

const auth = inject("auth");
const router = useRouter();
const route = useRoute();

const isAuth = computed(() => !!auth.token);
const dashboardPath = computed(() =>
  auth.role === "admin" ? "/admin/dashboard" : "/user/dashboard"
);
const isAdminRoute = computed(() => route.meta.layout === "admin");

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("role");
  auth.token = null;
  auth.role = null;
  router.push("/");
}
</script>

<style>
.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}
.nav-left {
  flex: 1;
  text-align: left;
}
.nav-center {
  flex: 1;
  text-align: center;
}
.nav-right {
  flex: 1;
  text-align: right;
}
</style>
