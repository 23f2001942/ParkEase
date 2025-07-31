<!-- frontend/src/views/AdminSummaryView.vue -->

<template>
  <div style="padding: 2rem">
    <h1>Admin Dashboard – Summary</h1>

    <section v-if="byLot.length">
      <h2>Revenue by Lot (this month)</h2>
      <BarChart
        :labels="byLot.map((l) => l.lot_name)"
        :values="byLot.map((l) => l.revenue_month)"
        label="₹ Revenue"
      />
    </section>

    <section v-if="byLot.length" style="margin-top: 2rem">
      <h2>Avg Occupancy by Lot</h2>
      <DoughnutChart
        :labels="byLot.map((l) => l.lot_name)"
        :values="byLot.map((l) => Math.round(l.occupied_pct * 100))"
      />
    </section>

    <section style="margin-top: 2rem">
      <p>
        <strong>Total Revenue (Month):</strong> ₹{{
          overall.total_revenue_month.toFixed(2)
        }}
      </p>
      <p>
        <strong>Avg Occupancy (All Lots):</strong>
        {{ (overall.avg_occupancy_pct * 100).toFixed(1) }}%
      </p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getAdminSummary } from "../services/api";
import BarChart from "../components/BarChart.vue";
import DoughnutChart from "../components/DoughnutChart.vue";

const byLot = ref([]);
const overall = ref({ total_revenue_month: 0, avg_occupancy_pct: 0 });

onMounted(async () => {
  try {
    const { data } = await getAdminSummary();
    byLot.value = data.by_lot;
    overall.value = data.overall;
  } catch (e) {
    console.error("Failed to load admin summary", e);
  }
});
</script>
