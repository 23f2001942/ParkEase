<!-- frontend/src/views/AdminDashboard.vue -->
<template>
  <div style="padding: 2rem">
    <h1>Parking Lots</h1>
    <div v-if="lots.length" class="lots-container">
      <div v-for="lot in lots" :key="lot.id" class="lot-box">
        <h3>{{ lot.name }}</h3>
        <small>
          <a @click="edit(lot.id)">Edit</a> |
          <a @click="del(lot.id)">Delete</a> |
          <a @click="viewSpots(lot.id)">Spots</a>
        </small>
        <p>Occupied: {{ lot.occupied_spots }} / {{ lot.total_spots }}</p>
      </div>
    </div>
    <p v-else>No parking lots found.</p>
    <button @click="goAdd">+ Add Lot</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const lots = ref([]);
const router = useRouter();

async function fetchLots() {
  try {
    const { data } = await api.get("/admin/lots");
    lots.value = Array.isArray(data)
      ? data
      : Array.isArray(data.lots)
      ? data.lots
      : [];
  } catch (e) {
    console.error("fetch lots failed:", e);
    lots.value = [];
  }
}

function goAdd() {
  router.push("/admin/lots/add");
}
function edit(id) {
  router.push(`/admin/lots/${id}/edit`);
}
function del(id) {
  if (!confirm("Delete this lot?")) return;
  api.delete(`/admin/lots/${id}`).then(fetchLots);
}
function viewSpots(id) {
  router.push(`/admin/lots/${id}/spots`);
}

onMounted(fetchLots);
</script>

<style>
.lots-container {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
.lot-box {
  border: 1px solid #ccc;
  padding: 1rem;
  width: 200px;
}
</style>
