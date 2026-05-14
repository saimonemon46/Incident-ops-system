import { useState } from 'react';
import { useIncidentStore } from '../store/incidentStore';

const emptyDraft = {
  title: '',
  description: '',
  severity: 'LOW',
  assigned_to: '',
};

export function useCreateIncident(onCreated) {
  const { addIncident } = useIncidentStore();
  const [draft, setDraft] = useState(emptyDraft);
  const [isSaving, setIsSaving] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setIsSaving(true);
    await addIncident({
      ...draft,
      assigned_to: draft.assigned_to.trim() || null,
    });
    setDraft(emptyDraft);
    setIsSaving(false);
    onCreated?.();
  }

  return { draft, isSaving, setDraft, submit };
}
