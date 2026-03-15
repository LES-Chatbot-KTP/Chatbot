/**
 * Authentication context — provides user state and login/logout functions.
 */
import React, { createContext, useState, useContext, useEffect } from 'react';
import { login as loginService, logout as logoutService, getMe, getToken } from '../services/authService';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  async function checkAuth() {
    try {
      const token = await getToken();
      if (token) {
        const userData = await getMe();
        setUser(userData);
      }
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  async function login(email, senha) {
    await loginService(email, senha);
    const userData = await getMe();
    setUser(userData);
  }

  async function logout() {
    await logoutService();
    setUser(null);
  }

  const isAdmin = user?.perfil_nome === 'administrador';

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAdmin }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
