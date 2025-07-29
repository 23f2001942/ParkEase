// frontend/src/main.js

import { createApp, reactive } from "vue";
import App from "./App.vue";
import router from "./router";

// Create a global reactive auth store
const auth = reactive({
  token: localStorage.getItem("access_token"),
  role: localStorage.getItem("role"),
});

const app = createApp(App);

// Provide it to all components
app.provide("auth", auth);

app.use(router).mount("#app");
