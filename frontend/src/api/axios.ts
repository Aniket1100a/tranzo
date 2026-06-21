import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

export const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Handle token refresh logic here if needed in the future
    if (error.response?.status === 401) {
      // Optional: handle unauthorized access (e.g., clear tokens and redirect to login)
      // localStorage.removeItem('access_token');
      // localStorage.removeItem('refresh_token');
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
