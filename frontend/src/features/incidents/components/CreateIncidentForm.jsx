import { SEVERITIES } from '../../../shared/constants/severity';
import Button from '../../../shared/components/ui/Button';
import Input from '../../../shared/components/ui/Input';
import { normalizeLabel } from '../utils/incidentHelpers';
import { useCreateIncident } from '../hooks/useCreateIncident';

export default function CreateIncidentForm({ onCreated }) {
  const { draft, isSaving, setDraft, submit } = useCreateIncident(onCreated);

  return (
    <form className="create-form" onSubmit={submit}>
      <Input
        id="incident-title"
        label="Title"
        minLength="3"
        required
        value={draft.title}
        onChange={(event) => setDraft({ ...draft, title: event.target.value })}
      />
      <label className="field" htmlFor="incident-severity">
        <span>Severity</span>
        <select
          id="incident-severity"
          value={draft.severity}
          onChange={(event) => setDraft({ ...draft, severity: event.target.value })}
        >
          {SEVERITIES.map((severity) => (
            <option key={severity} value={severity}>
              {normalizeLabel(severity)}
            </option>
          ))}
        </select>
      </label>
      <Input
        id="incident-owner"
        label="Owner"
        value={draft.assigned_to}
        onChange={(event) => setDraft({ ...draft, assigned_to: event.target.value })}
      />
      <Input
        as="textarea"
        id="incident-description"
        label="Description"
        minLength="10"
        required
        value={draft.description}
        onChange={(event) => setDraft({ ...draft, description: event.target.value })}
      />
      <Button disabled={isSaving} type="submit">
        {isSaving ? 'Saving...' : 'Create incident'}
      </Button>
    </form>
  );
}
