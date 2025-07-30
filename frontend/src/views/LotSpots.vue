<!-- frontend/src/views/LotSpots.vue -->

<template>
  <div style="padding: 2rem">
    <h1>Spots for "{{ lotName }}"</h1>

    <div v-if="Array.isArray(spots) && spots.length" class="spots-grid">
      <router-link
        v-for="spot in spots"
        :key="spot.id"
        :to="{ name: 'AdminSpotView', params: { spotId: spot.id } }"
        class="spot"
        :class="{ occupied: spot.status === 'O' }"
      >
        {{ spot.status === "O" ? "O" : "A" }}
      </router-link>
    </div>

    <p v-else>No spots found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "../services/api";

const route = useRoute();
const lotId = route.params.id;

const lotName = ref("");
const spots = ref([]);

async function fetchData() {
  try {
    // single call returns { id, name, …, spots: [ {id, spot_number, status}, … ] }
    const { data } = await api.get(`/admin/lots/${lotId}`);
    lotName.value = data.name;
    spots.value = Array.isArray(data.spots) ? data.spots : [];
  } catch (e) {
    console.error("fetch spots failed:", e);
    spots.value = [];
  }
}

onMounted(fetchData);
</script>

<style>
.spots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 40px);
  gap: 0.5rem;
  margin-top: 1rem;
}
.spot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1px solid #333;
  text-decoration: none;
  color: inherit;
}
.spot.occupied {
  background: #f88;
  color: #fff;
}
</style>
