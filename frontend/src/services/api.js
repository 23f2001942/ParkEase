// frontend/src/services/api.js

import axios from "axios";

const baseURL = process.env.VUE_APP_API_BASE_URL || "http://127.0.0.1:5000";
const api = axios.create({ baseURL });

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;

export function getAdminSummary() {
  return api.get("/admin/summary");
}

export function getUserSummary() {
  return api.get("/user/summary");
}
