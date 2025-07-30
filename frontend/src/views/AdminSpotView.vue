<!-- frontend/src/views/AdminSpotView.vue -->

<template>
  <div style="padding: 2rem">
    <h1>Spot #{{ spot.spot_number }} Details</h1>

    <div v-if="loaded">
      <p><strong>ID:</strong> {{ spot.id }}</p>
      <p><strong>Lot ID:</strong> {{ spot.lot_id }}</p>
      <p>
        <strong>Status:</strong>
        {{ spot.status === "O" ? "Occupied" : "Available" }}
      </p>

      <div v-if="spot.status === 'O'">
        <p><strong>User ID:</strong> {{ spot.user_id }}</p>
        <p><strong>Vehicle:</strong> {{ spot.vehicle_number }}</p>
        <p><strong>Started:</strong> {{ spot.parking_timestamp }}</p>
      </div>

      <button @click="deleteSpot" :disabled="spot.status === 'O'">
        Delete Spot
      </button>
      <p v-if="msg">{{ msg }}</p>
    </div>
    <p v-else>Loading…</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";

const route = useRoute();
const router = useRouter();
const spotId = route.params.spotId;

const spot = ref({});
const loaded = ref(false);
const msg = ref("");

async function loadSpot() {
  try {
    const { data } = await api.get(`/admin/spots/${spotId}`);
    spot.value = data;
  } catch (e) {
    console.error(e);
  } finally {
    loaded.value = true;
  }
}

async function deleteSpot() {
  try {
    const { data } = await api.delete(`/admin/spots/${spotId}`);
    msg.value = data.msg;
    if (data.msg === "Spot deleted") {
      // go back to dashboard after a second
      setTimeout(() => router.push("/admin/dashboard"), 800);
    }
  } catch (e) {
    msg.value = e.response?.data?.msg || "Delete failed";
  }
}

onMounted(loadSpot);
</script>
