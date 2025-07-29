<!-- frontend/src/views/UsersView.vue -->

<template>
  <div style="padding: 2rem">
    <h1>Registered Users</h1>

    <!-- only show the table if there's at least one user -->
    <table v-if="users.length" border="1" cellpadding="8">
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Full Name</th>
          <th>Address</th>
          <th>Pin Code</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.full_name }}</td>
          <td>{{ u.address }}</td>
          <td>{{ u.pin_code }}</td>
        </tr>
      </tbody>
    </table>

    <!-- fallback when empty -->
    <p v-else>No users found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const users = ref([]);

async function fetchUsers() {
  try {
    const { data } = await api.get("/admin/users");
    // support either { users: [...] } or plain array
    users.value = Array.isArray(data.users)
      ? data.users
      : Array.isArray(data)
      ? data
      : [];
  } catch (e) {
    console.error("fetch users failed:", e);
    users.value = [];
  }
}

onMounted(fetchUsers);
</script>
