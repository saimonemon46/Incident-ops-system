import { apiRequest } from '../../../shared/services/axios';

export function listIncidents() {
  return apiRequest('/incidents/?limit=100');
}

export function createIncident(payload) {
  return apiRequest('/incidents/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateIncident(id, payload) {
  return apiRequest(`/incidents/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}
