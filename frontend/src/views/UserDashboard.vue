<!-- frontend/src/views/UserDashboard.vue -->

<template>
  <div style="padding: 2rem">
    <h1>Your Parking History</h1>
    <table border="1" cellpadding="8">
      <thead>
        <tr>
          <th>Lot ID</th>
          <th>Spot #</th>
          <th>Vehicle</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Cost</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in reservations" :key="r.reservation_id">
          <td>{{ r.lot_id }}</td>
          <td>{{ r.spot_id }}</td>
          <td>{{ r.vehicle_number }}</td>
          <td>{{ r.start_time }}</td>
          <td>{{ r.end_time || "—" }}</td>
          <td>
            {{ r.parking_cost != null ? r.parking_cost.toFixed(2) : "—" }}
          </td>
          <td>{{ r.status }}</td>
          <td>
            <router-link
              v-if="r.status === 'ongoing'"
              :to="`/user/release/${r.reservation_id}`"
            >
              Release
            </router-link>
            <span v-else>—</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const reservations = ref([]);

async function fetchHistory() {
  try {
    const { data } = await api.get("/user/reservations");
    reservations.value = data.reservations;
  } catch (e) {
    console.error("Failed to load reservations:", e);
    reservations.value = [];
  }
}

onMounted(fetchHistory);
</script>
