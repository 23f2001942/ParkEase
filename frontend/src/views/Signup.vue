<!-- frontend/src/views/Signup.vue -->

<template>
  <div class="auth-form">
    <h2>Sign Up</h2>
    <form @submit.prevent="onSignup">
      <div>
        <label>Email:</label><input v-model="email" type="email" required />
      </div>
      <div>
        <label>Password:</label
        ><input v-model="password" type="password" required />
      </div>
      <div><label>Full Name:</label><input v-model="full_name" required /></div>
      <div><label>Address:</label><textarea v-model="address" required /></div>
      <div><label>Pin Code:</label><input v-model="pin_code" required /></div>
      <button type="submit">Register</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const email = ref("");
const password = ref("");
const full_name = ref("");
const address = ref("");
const pin_code = ref("");
const error = ref(null);
const message = ref(null);
const router = useRouter();

async function onSignup() {
  error.value = null;
  message.value = null;
  try {
    await api.post("/auth/register", {
      email,
      password,
      full_name,
      address,
      pin_code,
    });
    message.value = "Registered successfully! Redirecting to login…";
    setTimeout(() => router.push("/login"), 1500);
  } catch (e) {
    error.value = e.response?.data?.msg || "Registration failed";
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
.message {
  color: green;
}
</style>
