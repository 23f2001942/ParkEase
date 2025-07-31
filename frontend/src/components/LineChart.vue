<template>
  <canvas ref="canvas"></canvas>
</template>
<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
  labels: Array,
  values: Array,
  label: { type: String, default: "Value" },
});

const canvas = ref(null);

onMounted(() => {
  new Chart(canvas.value.getContext("2d"), {
    type: "line",
    data: {
      labels: props.labels,
      datasets: [
        {
          label: props.label,
          data: props.values,
          fill: false,
        },
      ],
    },
    options: { responsive: true },
  });
});
</script>
