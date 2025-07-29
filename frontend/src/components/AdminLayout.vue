<!-- frontend/src/components/AdminLayout.vue -->

<template>
  <div>
    <!-- ADMIN NAVBAR -->
    <div class="admin-nav">
      <strong>Welcome, Admin!</strong>
      <router-link to="/admin/dashboard">Home</router-link> |
      <router-link to="/admin/users">Users</router-link> |
      <router-link to="/admin/search">Search</router-link> |
      <router-link to="/admin/summary">Summary</router-link> |
      <a href="#" @click.prevent="logout">Logout</a>
    </div>

    <!-- nested admin view -->
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
  padding: 1rem;
  background: #f3f3f3;
  border-bottom: 1px solid #ccc;
}
</style>
