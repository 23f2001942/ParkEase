<!-- frontend/src/views/HomeView.vue -->

<template>
  <div class="home-view">
    <h1>Welcome to ParkEase</h1>
    <p>Your hassle-free parking solution</p>
    <div v-if="!isAuth" class="home-actions">
      <router-link to="/login"><button>Login</button></router-link>
      <router-link to="/signup"><button>Sign Up</button></router-link>
    </div>
    <div v-else class="home-actions">
      <router-link :to="dashboardPath">
        <button>Go to Dashboard</button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
const isAuth = computed(() => !!localStorage.getItem("access_token"));
const dashboardPath = computed(() =>
  localStorage.getItem("role") === "admin"
    ? "/admin/dashboard"
    : "/user/dashboard"
);
</script>

<style>
.home-view {
  text-align: center;
  padding: 2rem;
}
.home-actions button {
  margin: 0 0.5rem;
}
</style>
