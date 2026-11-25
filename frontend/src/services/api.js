
import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 10000,
});

export const checkBackend = async () => {
  const response = await API.get("/health");
  return response.data;
};

export default API;
