import { createContext, useCallback, useEffect, useMemo, useState } from 'react';
import { getStoredUser, getToken, setStoredUser, setToken } from '../../../shared/services/authToken';
import * as authApi from '../api/authApi';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setAuthToken] = useState(getToken);
  const [user, setUser] = useState(getStoredUser);
  const [isBooting, setIsBooting] = useState(Boolean(token));

  const saveSession = useCallback((session) => {
    setToken(session.access_token);
    setStoredUser(session.user);
    setAuthToken(session.access_token);
    setUser(session.user);
  }, []);

  const logout = useCallback(() => {
    setToken('');
    setStoredUser(null);
    setAuthToken('');
    setUser(null);
    window.location.hash = '#/login';
  }, []);

  useEffect(() => {
    let isMounted = true;

    async function loadProfile() {
      if (!token) {
        setIsBooting(false);
        return;
      }

      try {
        const profile = await authApi.me();
        if (isMounted) {
          setUser(profile);
          setStoredUser(profile);
        }
      } catch {
        if (isMounted) {
          logout();
        }
      } finally {
        if (isMounted) {
          setIsBooting(false);
        }
      }
    }

    loadProfile();
    return () => {
      isMounted = false;
    };
  }, [logout, token]);

  const value = useMemo(
    () => ({
      isAuthenticated: Boolean(token),
      isBooting,
      login: authApi.login,
      logout,
      register: authApi.register,
      saveSession,
      token,
      user,
    }),
    [isBooting, logout, saveSession, token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
