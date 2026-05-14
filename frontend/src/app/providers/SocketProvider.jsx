import { createContext, useMemo } from 'react';
import { createSocketClient } from '../../shared/services/socket';

export const SocketContext = createContext(null);

export function SocketProvider({ children }) {
  const socket = useMemo(() => createSocketClient(), []);

  return <SocketContext.Provider value={socket}>{children}</SocketContext.Provider>;
}
