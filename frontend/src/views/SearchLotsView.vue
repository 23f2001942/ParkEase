<!-- frontend/src/views/SearchLotsView.vue -->

<template>
  <div style="padding: 2rem; max-width: 600px; margin: auto">
    <h1>Search Parking Lots</h1>

    <form @submit.prevent="onSearch" style="margin-bottom: 1rem">
      <label>Location:</label>
      <input v-model="location" placeholder="City or street" />
      <label style="margin-left: 1rem">Pin Code:</label>
      <input v-model="pin_code" placeholder="e.g. 560001" />
      <button type="submit" style="margin-left: 1rem">Search</button>
    </form>

    <table v-if="lots.length" border="1" cellpadding="8">
      <thead>
        <tr>
          <th>Lot ID</th>
          <th>Name</th>
          <th>Address</th>
          <th>Price/hr</th>
          <th>Avail Spots</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="l in lots" :key="l.id">
          <td>{{ l.id }}</td>
          <td>{{ l.name }}</td>
          <td>{{ l.address }}</td>
          <td>{{ l.price_per_hour }}</td>
          <td>{{ l.available_spots }}</td>
          <td>
            <router-link :to="`/user/book/${l.id}`">Book</router-link>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>No lots found.</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../services/api";

const location = ref("");
const pin_code = ref("");
const lots = ref([]);

async function onSearch() {
  try {
    const params = {};
    if (location.value) params.location = location.value;
    if (pin_code.value) params.pin_code = pin_code.value;
    const { data } = await api.get("/user/lots", { params });
    lots.value = data.lots;
  } catch (e) {
    console.error("Search failed:", e);
    lots.value = [];
  }
}
</script>
