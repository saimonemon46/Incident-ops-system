import { useContext } from 'react';
import { SocketContext } from '../../app/providers/SocketProvider';

export function useSocket() {
  return useContext(SocketContext);
}
