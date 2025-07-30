<template>
  <div style="padding: 2rem; max-width: 400px; margin: auto">
    <h1>Book Lot #{{ lotId }}</h1>

    <form @submit.prevent="onBook">
      <div>
        <label>Vehicle Number:</label><br />
        <input v-model="vehicle" required />
      </div>
      <div style="margin-top: 1rem">
        <button type="submit">Confirm Booking</button>
        <button type="button" @click="cancel" style="margin-left: 1rem">
          Cancel
        </button>
      </div>
      <p v-if="error" style="color: red">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";

const route = useRoute();
const router = useRouter();
const lotId = route.params.lot_id;

const vehicle = ref("");
const error = ref(null);

async function onBook() {
  error.value = null;
  try {
    await api.post("/user/reserve", {
      lot_id: lotId,
      vehicle_number: vehicle.value,
    });
    router.push("/user/dashboard");
  } catch (e) {
    console.error("Booking failed:", e);
    error.value = e.response?.data?.msg || "Booking failed";
  }
}

function cancel() {
  router.push("/user/dashboard");
}
</script>
