<!-- frontend/src/views/UserDashboard.vue -->

<template>
  <div class="user-dashboard">
    <h1>User Dashboard</h1>
    <p>Welcome back, {{ fullName }}!</p>
  </div>
</template>

<script setup>
import { computed } from "vue";
const fullName = computed(() => localStorage.getItem("full_name") || "User");
</script>

<style>
.user-dashboard {
  text-align: center;
  padding: 2rem;
}
</style>
