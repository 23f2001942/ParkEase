<template>
  <div style="padding: 2rem; max-width: 600px; margin: auto">
    <h1>New Parking Lot</h1>
    <form @submit.prevent="onSubmit">
      <div>
        <label>Name:</label><br />
        <input v-model="name" required />
      </div>

      <div style="margin-top: 0.5rem">
        <label>Address:</label><br />
        <textarea v-model="address" required></textarea>
      </div>

      <div style="margin-top: 0.5rem">
        <label>Pin Code:</label><br />
        <input v-model="pin_code" required />
      </div>

      <div style="margin-top: 0.5rem">
        <label>Price per Hour:</label><br />
        <input type="number" v-model.number="price_per_hour" required />
      </div>

      <div style="margin-top: 0.5rem">
        <label>Total Spots:</label><br />
        <input type="number" v-model.number="total_spots" required />
      </div>

      <div style="margin-top: 1rem">
        <button type="submit">Add</button>
        <button type="button" @click="cancel">Cancel</button>
      </div>

      <p v-if="error" style="color: red">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const name = ref("");
const address = ref("");
const pin_code = ref("");
const price_per_hour = ref(0);
const total_spots = ref(0);
const error = ref(null);

const router = useRouter();

async function onSubmit() {
  error.value = null;
  try {
    await api.post("/admin/lots", {
      name: name.value,
      address: address.value,
      pin_code: pin_code.value,
      price_per_hour: price_per_hour.value,
      total_spots: total_spots.value,
    });
    router.push("/admin/dashboard");
  } catch (e) {
    console.error(e);
    error.value = e.response?.data?.msg || "Failed to add lot";
  }
}

function cancel() {
  router.push("/admin/dashboard");
}
</script>
