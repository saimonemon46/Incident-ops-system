import { apiRequest } from '../../../shared/services/axios';

export function runTriage(incidentId) {
  return apiRequest(`/incidents/${incidentId}/triage`, {
    method: 'POST',
  });
}
