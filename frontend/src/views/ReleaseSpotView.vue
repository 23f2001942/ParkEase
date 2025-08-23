<!-- frontend/src/views/ReleaseSpotView.vue -->

<template>
  <div style="padding: 2rem">
    <h1>Release Parking Spot</h1>
    <p>Spot ID: {{ spotId }}</p>
    <p>Lot ID: {{ lotId }}</p>
    <p>Vehicle: {{ vehicle }}</p>
    <p>Start Time: {{ startTime }}</p>
    <p>Releasing Time: {{ releaseTime || "—" }}</p>
    <p>
      Price / hour: {{ pricePerHour != null ? pricePerHour.toFixed(2) : "—" }}
    </p>
    <p>Total Cost: {{ totalCost != null ? totalCost.toFixed(2) : "—" }}</p>

    <button :disabled="released" @click="doRelease">Release Spot</button>
    <button @click="$router.back()">Cancel</button>

    <p v-if="message" :style="{ color: released ? 'green' : 'red' }">
      {{ message }}
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "../services/api";

const route = useRoute();

const resId = route.params.res_id;

const spotId = ref(null);
const lotId = ref(null);
const vehicle = ref("");
const startTime = ref("");
const releaseTime = ref("");
const pricePerHour = ref(null);
const totalCost = ref(null);
const message = ref("");
const released = ref(false);

async function fetchData() {
  try {
    const { data } = await api.get("/user/reservations");
    const r = data.reservations.find((x) => x.reservation_id === +resId);
    if (!r) throw new Error("Reservation not found");

    spotId.value = r.spot_id;
    lotId.value = r.lot_id;
    vehicle.value = r.vehicle_number;
    startTime.value = r.start_time;
    releaseTime.value = r.end_time || "";

    const lotResp = await api.get(`/user/lots/${lotId.value}`);
    pricePerHour.value = lotResp.data.price_per_hour;

    if (releaseTime.value) computeCost();
    if (r.status !== "ongoing") released.value = true;
  } catch (err) {
    message.value = err.response?.data?.msg || err.message;
  }
}

function computeCost() {
  const start = new Date(startTime.value);
  const end = new Date(releaseTime.value);
  const hours = (end - start) / (1000 * 60 * 60);
  totalCost.value = hours * pricePerHour.value;
}

async function doRelease() {
  try {
    const resp = await api.post(`/user/reservations/${resId}/release`);
    releaseTime.value = resp.data.end_time;
    released.value = true;

    computeCost();

    message.value = `Released! Total cost ₹${totalCost.value.toFixed(2)}`;
  } catch (err) {
    message.value = err.response?.data?.msg || "Release failed";
  }
}

onMounted(fetchData);
</script>
