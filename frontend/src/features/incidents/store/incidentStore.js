import { createContext, useCallback, useContext, useMemo, useState } from 'react';
import { sampleIncidents } from '../utils/incidentHelpers';
import * as incidentApi from '../api/incidentApi';

const IncidentContext = createContext(null);

export function IncidentProvider({ children }) {
  const [incidents, setIncidents] = useState(sampleIncidents);
  const [selectedId, setSelectedId] = useState(sampleIncidents[0].id);
  const [notice, setNotice] = useState('Showing demo incidents until live data loads.');
  const [isLoading, setIsLoading] = useState(false);

  const refreshIncidents = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await incidentApi.listIncidents();
      setIncidents(data.length ? data : sampleIncidents);
      setSelectedId(data[0]?.id || sampleIncidents[0].id);
      setNotice(data.length ? `Loaded ${data.length} live incidents.` : 'No live incidents yet. Demo queue is visible.');
    } catch (error) {
      setNotice(`${error.message}. Demo queue is visible.`);
      setIncidents(sampleIncidents);
      setSelectedId(sampleIncidents[0].id);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const addIncident = useCallback(async (payload) => {
    try {
      const created = await incidentApi.createIncident(payload);
      setIncidents((current) => [created, ...current]);
      setSelectedId(created.id);
      setNotice('Incident created.');
      return created;
    } catch (error) {
      const localIncident = {
        ...payload,
        id: `draft-${Date.now()}`,
        status: 'OPEN',
        category: 'UNKNOWN',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setIncidents((current) => [localIncident, ...current]);
      setSelectedId(localIncident.id);
      setNotice(`${error.message}. Created a local draft instead.`);
      return localIncident;
    }
  }, []);

  const updateIncident = useCallback(async (incident, payload) => {
    const localOnly = incident.id.startsWith('sample-') || incident.id.startsWith('draft-');

    if (localOnly) {
      setIncidents((current) =>
        current.map((item) =>
          item.id === incident.id ? { ...item, ...payload, updated_at: new Date().toISOString() } : item
        )
      );
      setNotice('Updated incident locally.');
      return;
    }

    try {
      const updated = await incidentApi.updateIncident(incident.id, payload);
      setIncidents((current) => current.map((item) => (item.id === updated.id ? updated : item)));
      setNotice('Incident updated.');
    } catch (error) {
      setNotice(error.message);
    }
  }, []);

  const selectedIncident = incidents.find((incident) => incident.id === selectedId) || incidents[0];

  const value = useMemo(
    () => ({
      addIncident,
      incidents,
      isLoading,
      notice,
      refreshIncidents,
      selectedId,
      selectedIncident,
      setIncidents,
      setNotice,
      setSelectedId,
      updateIncident,
    }),
    [addIncident, incidents, isLoading, notice, refreshIncidents, selectedId, selectedIncident, updateIncident]
  );

  return <IncidentContext.Provider value={value}>{children}</IncidentContext.Provider>;
}

export function useIncidentStore() {
  const context = useContext(IncidentContext);
  if (!context) {
    throw new Error('useIncidentStore must be used inside IncidentProvider');
  }

  return context;
}
