import { useEffect } from 'react';
import { useIncidentStore } from '../store/incidentStore';

export function useIncidents() {
  const store = useIncidentStore();
  const { refreshIncidents } = store;

  useEffect(() => {
    refreshIncidents();
  }, [refreshIncidents]);

  return store;
}
