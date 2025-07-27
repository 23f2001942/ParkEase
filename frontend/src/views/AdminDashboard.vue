<!-- frontend/src/views/AdminDashboard.vue -->

<template>
  <div style="text-align: center; margin: 2rem">
    <h2>Admin Dashboard</h2>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import api from "../services/api";

export default {
  setup() {
    const msg = ref("Loading…");
    onMounted(async () => {
      try {
        const { data } = await api.get("/admin/dashboard");
        msg.value = data.msg;
      } catch {
        msg.value = "Failed to load dashboard";
      }
    });
    return { msg };
  },
};
</script>
