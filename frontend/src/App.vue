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

<script>
import { computed } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const isAuth = computed(() => !!localStorage.getItem("access_token"));
    const role = computed(() => localStorage.getItem("role"));
    const dashboardPath = computed(() => {
      return role.value === "admin" ? "/admin/dashboard" : "/user/dashboard";
    });

    function logout() {
      localStorage.clear();
      router.push("/");
    }

    return { isAuth, dashboardPath, logout };
  },
};
</script>
