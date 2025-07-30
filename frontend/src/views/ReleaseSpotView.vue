<!-- frontend/src/views/ReleaseSpotView.vue -->

<template>
  <div style="padding: 2rem; max-width: 400px; margin: auto">
    <h1>Release Reservation #{{ resId }}</h1>
    <p>Are you sure you want to release this spot?</p>
    <button @click="onRelease">Yes, Release</button>
    <button @click="cancel" style="margin-left: 1rem">Cancel</button>
    <p v-if="error" style="color: red">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";

const route = useRoute();
const router = useRouter();
const resId = route.params.res_id;

const error = ref(null);

async function onRelease() {
  error.value = null;
  try {
    await api.post(`/user/reservations/${resId}/release`);
    router.push("/user/dashboard");
  } catch (e) {
    console.error("Release failed:", e);
    error.value = e.response?.data?.msg || "Release failed";
  }
}

function cancel() {
  router.push("/user/dashboard");
}
</script>
