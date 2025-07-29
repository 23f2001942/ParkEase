<template>
  <div style="padding: 2rem">
    <h1>Spots for "{{ lotName }}"</h1>

    <div v-if="Array.isArray(spots) && spots.length" class="spots-grid">
      <div
        v-for="spot in spots"
        :key="spot.id"
        class="spot"
        :class="{ occupied: spot.status === 'occupied' }"
      >
        {{ spot.status }}
      </div>
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
    // fetch lot info
    const { data: lot } = await api.get(`/admin/lots/${lotId}`);
    lotName.value = lot.name;
    // fetch spots
    const { data: s } = await api.get(`/admin/lots/${lotId}/spots`);
    spots.value = Array.isArray(s.spots) ? s.spots : s;
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
  width: 40px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  border: 1px solid #333;
  cursor: default;
}
.spot.occupied {
  background: #f88;
  color: white;
}
</style>
