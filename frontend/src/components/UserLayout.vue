<!-- frontend/src/components/UserLayout.vue -->

<template>
  <div>
    <nav class="user-nav">
      <div class="nav-left">Welcome, User!</div>
      <div class="nav-right">
        <router-link to="/user/dashboard">Home</router-link> |
        <router-link to="/user/search">Search Lots</router-link> |
        <router-link to="/user/summary">Summary</router-link> |
        <a href="#" @click.prevent="logout">Logout</a>
      </div>
    </nav>
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
.user-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}
.user-nav span {
  font-weight: bold;
}
.user-nav a,
.user-nav .router-link-active {
  margin: 0 0.5rem;
}
</style>
