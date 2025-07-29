<!-- frontend/src/views/Login.vue -->

<template>
  <div style="max-width: 400px; margin: 2rem auto">
    <h2>Login</h2>
    <form @submit.prevent="onLogin">
      <div>
        <label>Email:</label><br />
        <input v-model="email" type="email" required />
      </div>
      <div style="margin-top: 0.5rem">
        <label>Password:</label><br />
        <input v-model="password" type="password" required />
      </div>
      <div style="margin-top: 1rem">
        <button type="submit">Login</button>
      </div>
    </form>
    <p v-if="error" style="color: red">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, inject } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const error = ref(null);
const router = useRouter();

// Inject the reactive auth store
const auth = inject("auth");

async function onLogin() {
  error.value = null;
  try {
    const { data } = await api.post("/auth/login", {
      email: email.value,
      password: password.value,
    });

    // 1) Persist to localStorage
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("role", data.role);

    // 2) Update reactive store
    auth.token = data.access_token;
    auth.role = data.role;

    // 3) Redirect to appropriate dashboard
    router.push(data.role === "admin" ? "/admin/dashboard" : "/user/dashboard");
  } catch (err) {
    error.value = err.response?.data?.msg || "Login failed";
  }
}
</script>
