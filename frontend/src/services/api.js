import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
};

// OLT API
export const oltAPI = {
  getAll: () => api.get('/olt/'),
  getById: (id) => api.get(`/olt/${id}`),
  create: (data) => api.post('/olt/', data),
  update: (id, data) => api.put(`/olt/${id}`, data),
  delete: (id) => api.delete(`/olt/${id}`),
  test: (id) => api.post(`/olt/${id}/test`),
  sync: (id) => api.post(`/olt/${id}/sync`),
};

// ONU API
export const onuAPI = {
  getAll: (params) => api.get('/onu/', { params }),
  getById: (id) => api.get(`/onu/${id}`),
  create: (data) => api.post('/onu/', data),
  update: (id, data) => api.put(`/onu/${id}`, data),
  delete: (id) => api.delete(`/onu/${id}`),
  refresh: (id) => api.post(`/onu/${id}/refresh`),
  discover: (oltId) => api.get(`/onu/olt/${oltId}/discover`),
};

// ODP API
export const odpAPI = {
  getAll: () => api.get('/odp/'),
  getById: (id) => api.get(`/odp/${id}`),
  create: (data) => api.post('/odp/', data),
  update: (id, data) => api.put(`/odp/${id}`, data),
  delete: (id) => api.delete(`/odp/${id}`),
};

// Cable Route API
export const cableRouteAPI = {
  getAll: () => api.get('/cable-route/'),
  getById: (id) => api.get(`/cable-route/${id}`),
  create: (data) => api.post('/cable-route/', data),
  delete: (id) => api.delete(`/cable-route/${id}`),
};

// Dashboard API
export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
  getRecentOnus: () => api.get('/dashboard/recent-onus'),
  getAlerts: () => api.get('/dashboard/alerts'),
};

export default api;
