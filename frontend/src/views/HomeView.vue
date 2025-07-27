<!-- frontend/src/views/HomeView.vue -->

<template>
  <div style="text-align: center; padding: 2rem">
    <h1>Welcome to ParkEase</h1>
    <p>Your hassle-free parking solution</p>

    <div v-if="!isAuth" style="margin-top: 1rem">
      <router-link to="/login"><button>Login</button></router-link>
      <router-link to="/signup"><button>Sign Up</button></router-link>
    </div>
    <div v-else style="margin-top: 1rem">
      <router-link :to="dashboardPath"
        ><button>Go to Dashboard</button></router-link
      >
    </div>
  </div>
</template>

<script>
import { computed } from "vue";

export default {
  setup() {
    const isAuth = computed(() => !!localStorage.getItem("access_token"));
    const role = computed(() => localStorage.getItem("role"));
    const dashboardPath = computed(() =>
      role.value === "admin" ? "/admin/dashboard" : "/user/dashboard"
    );
    return { isAuth, dashboardPath };
  },
};
</script>
