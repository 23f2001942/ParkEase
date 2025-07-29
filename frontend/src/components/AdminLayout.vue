<!-- frontend/src/components/AdminLayout.vue -->

<template>
  <div>
    <!-- ADMIN NAVBAR -->
    <div class="admin-nav">
      <div class="nav-left">Welcome, Admin!</div>
      <div class="nav-center">
        <router-link to="/admin/dashboard">Home</router-link> |
        <router-link to="/admin/users">Users</router-link> |
        <router-link to="/admin/search">Search</router-link> |
        <router-link to="/admin/summary">Summary</router-link> |
        <a href="#" @click.prevent="logout">Logout</a>
      </div>
    </div>
    <router-view />
  </div>
</template>

<script setup>
import { inject } from "vue";
import { useRouter } from "vue-router";

const auth = inject("auth");
const router = useRouter();

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("role");
  auth.token = null;
  auth.role = null;
  router.push("/");
}
</script>

<style>
.admin-nav {
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
