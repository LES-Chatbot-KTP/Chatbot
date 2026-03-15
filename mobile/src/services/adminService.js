/**
 * Admin service — documents, users, metrics, logs.
 */
import api from './api';

// Users
export async function listUsuarios() {
  const response = await api.get('/usuarios/');
  return response.data;
}

export async function createUsuario(data) {
  const response = await api.post('/usuarios/', data);
  return response.data;
}

// Documents
export async function listDocumentos() {
  const response = await api.get('/documentos/');
  return response.data;
}

export async function createDocumento(data) {
  const response = await api.post('/documentos/', data);
  return response.data;
}

export async function updateDocumento(id, data) {
  const response = await api.put(`/documentos/${id}`, data);
  return response.data;
}

export async function getDocumento(id) {
  const response = await api.get(`/documentos/${id}`);
  return response.data;
}

export async function reindexDocumento(id) {
  const response = await api.post(`/documentos/${id}/indexar`);
  return response.data;
}

// Categories
export async function listCategorias() {
  const response = await api.get('/documentos/categorias');
  return response.data;
}

export async function createCategoria(data) {
  const response = await api.post('/documentos/categorias', data);
  return response.data;
}

// Metrics & Logs
export async function getMetricas() {
  const response = await api.get('/admin/metricas');
  return response.data;
}

export async function getLogs() {
  const response = await api.get('/admin/logs');
  return response.data;
}
