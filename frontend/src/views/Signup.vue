<!-- frontend/src/views/Signup.vue -->

<template>
  <div style="max-width: 400px; margin: 2rem auto">
    <h2>Sign Up</h2>
    <form @submit.prevent="onSignup">
      <div>
        <label>Email:</label><br />
        <input v-model="email" type="email" required />
      </div>
      <div style="margin-top: 0.5rem">
        <label>Password:</label><br />
        <input v-model="password" type="password" required />
      </div>
      <div style="margin-top: 0.5rem">
        <label>Full Name:</label><br />
        <input v-model="full_name" required />
      </div>
      <div style="margin-top: 0.5rem">
        <label>Address:</label><br />
        <textarea v-model="address" required></textarea>
      </div>
      <div style="margin-top: 0.5rem">
        <label>Pin Code:</label><br />
        <input v-model="pin_code" required />
      </div>
      <div style="margin-top: 1rem">
        <button type="submit">Register</button>
      </div>
    </form>
    <p v-if="error" style="color: red">{{ error }}</p>
    <p v-if="message" style="color: green">{{ message }}</p>
  </div>
</template>

<script>
import { ref } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

export default {
  setup() {
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
      try {
        await api.post("/auth/register", {
          email: email.value,
          password: password.value,
          full_name: full_name.value,
          address: address.value,
          pin_code: pin_code.value,
        });
        message.value = "Registered successfully! Redirecting to login…";
        setTimeout(() => router.push("/login"), 1500);
      } catch (err) {
        error.value = err.response?.data?.msg || "Registration failed";
      }
    }

    return {
      email,
      password,
      full_name,
      address,
      pin_code,
      error,
      message,
      onSignup,
    };
  },
};
</script>
