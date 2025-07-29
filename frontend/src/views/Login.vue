<!-- frontend/src/views/Login.vue -->

<template>
  <div class="auth-form">
    <h2>Login</h2>
    <form @submit.prevent="onLogin">
      <div>
        <label>Email:</label><input v-model="email" type="email" required />
      </div>
      <div>
        <label>Password:</label
        ><input v-model="password" type="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, inject } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const email = ref("");
const password = ref("");
const error = ref(null);
const router = useRouter();
const auth = inject("auth");

async function onLogin() {
  error.value = null;
  try {
    const { data } = await api.post("/auth/login", {
      email: email.value,
      password: password.value,
    });
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("role", data.role);
    auth.token = data.access_token;
    auth.role = data.role;
    router.push(data.role === "admin" ? "/admin/dashboard" : "/user/dashboard");
  } catch (e) {
    error.value = e.response?.data?.msg || "Login failed";
  }
}
</script>

<style>
.auth-form {
  max-width: 400px;
  margin: 2rem auto;
}
.auth-form div {
  margin-bottom: 1rem;
}
.error {
  color: red;
}
</style>
