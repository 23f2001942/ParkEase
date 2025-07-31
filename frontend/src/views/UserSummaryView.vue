<!-- frontend/src/views/UserSummaryView.vue -->

<template>
  <div style="padding: 2rem">
    <h1>Your Summary</h1>

    <section>
      <p>
        <strong>Total Spent (All Time):</strong> ₹{{
          summary.total_spent.toFixed(2)
        }}
      </p>
      <p>
        <strong>Spent This Month:</strong> ₹{{
          summary.monthly_spent.toFixed(2)
        }}
      </p>
      <p><strong>Reservations Made:</strong> {{ summary.history_count }}</p>
    </section>

    <section v-if="summary.by_month.length" style="margin-top: 2rem">
      <h2>Monthly Spend</h2>
      <LineChart
        :labels="summary.by_month.map((m) => m.month)"
        :values="summary.by_month.map((m) => m.spent)"
        label="₹ Spent"
      />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getUserSummary } from "../services/api";
import LineChart from "../components/LineChart.vue";

const summary = ref({
  history_count: 0,
  total_spent: 0,
  monthly_spent: 0,
  by_month: [],
});

onMounted(async () => {
  try {
    const { data } = await getUserSummary();
    summary.value = data;
  } catch (e) {
    console.error("Failed to load user summary", e);
  }
});
</script>
