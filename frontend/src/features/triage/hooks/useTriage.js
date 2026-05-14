import { useState } from 'react';
import { useIncidentStore } from '../../incidents/store/incidentStore';
import * as triageApi from '../api/triageApi';

export function useTriage() {
  const { setIncidents, setNotice } = useIncidentStore();
  const [isRunning, setIsRunning] = useState(false);

  async function run(incident) {
    if (!incident) {
      return;
    }

    if (incident.id.startsWith('sample-') || incident.id.startsWith('draft-')) {
      setNotice('Triage preview is available for live API incidents.');
      return;
    }

    setIsRunning(true);
    try {
      const result = await triageApi.runTriage(incident.id);
      setIncidents((current) =>
        current.map((item) =>
          item.id === incident.id
            ? {
                ...item,
                category: result.triage.category,
                severity: result.triage.severity,
                suggested_fix: result.triage.suggested_fix,
                ai_notes: result.triage.ai_notes,
              }
            : item
        )
      );
      setNotice(result.message);
    } catch (error) {
      setNotice(error.message);
    } finally {
      setIsRunning(false);
    }
  }

  return { isRunning, run };
}
