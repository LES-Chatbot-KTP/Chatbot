/**
 * Authentication service — login, logout, token management.
 */
import api from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export async function login(email, senha) {
  const response = await api.post('/auth/login', { email, senha });
  const { access_token } = response.data;
  await AsyncStorage.setItem('access_token', access_token);
  return access_token;
}

export async function logout() {
  await AsyncStorage.removeItem('access_token');
}

export async function getMe() {
  const response = await api.get('/auth/me');
  return response.data;
}

export async function getToken() {
  return AsyncStorage.getItem('access_token');
}
