<!-- frontend/src/App.vue -->

<template>
  <div>
    <nav style="padding: 1rem; border-bottom: 1px solid #eee">
      <router-link to="/">Home</router-link> |
      <template v-if="!isAuth">
        <router-link to="/login">Login</router-link> |
        <router-link to="/signup">Sign Up</router-link>
      </template>
      <template v-else>
        <router-link :to="dashboardPath">Dashboard</router-link> |
        <a href="#" @click.prevent="logout">Logout</a>
      </template>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { inject, computed } from "vue";
import { useRouter } from "vue-router";

// Inject the shared auth store
const auth = inject("auth");
const router = useRouter();

// Reactive computed props
const isAuth = computed(() => !!auth.token);
const dashboardPath = computed(() =>
  auth.role === "admin" ? "/admin/dashboard" : "/user/dashboard"
);

// Logout handler clears both localStorage and reactive state
function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("role");
  auth.token = null;
  auth.role = null;
  router.push("/");
}
</script>
