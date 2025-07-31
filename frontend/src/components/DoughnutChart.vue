<!-- frontend/src/components/DoughnutChart.vue -->

<template>
  <canvas ref="canvas"></canvas>
</template>
<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
  labels: Array,
  values: Array,
});

const canvas = ref(null);

onMounted(() => {
  new Chart(canvas.value.getContext("2d"), {
    type: "doughnut",
    data: {
      labels: props.labels,
      datasets: [{ data: props.values }],
    },
    options: { responsive: true },
  });
});
</script>
