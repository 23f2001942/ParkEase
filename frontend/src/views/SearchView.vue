<!-- frontend/src/views/SearchView.vue -->

<template>
  <div style="padding: 2rem">
    <h1>Search</h1>
    <div>
      <select v-model="field">
        <option value="user">User ID</option>
        <option value="lot">Lot Name</option>
        <option value="spot">Spot Number</option>
      </select>
      <input v-model="term" placeholder="Enter search term" />
      <button @click="onSearch">Search</button>
    </div>
    <div v-if="results.length" style="margin-top: 1rem">
      <h2>Results</h2>
      <pre>{{ results }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const field = ref("user");
const term = ref("");
const results = ref([]);

function onSearch() {
  // hook into your real API later
  results.value = [{ field: field.value, term: term.value }];
}
</script>
