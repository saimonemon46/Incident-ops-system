import Button from '../../../shared/components/ui/Button';
import AISummary from './AISummary';
import RootCauseCard from './RootCauseCard';
import SuggestedFixes from './SuggestedFixes';
import { useTriage } from '../hooks/useTriage';

export default function TriagePanel({ incident }) {
  const { isRunning, run } = useTriage();

  return (
    <section className="triage-card">
      <AISummary incident={incident} />
      <RootCauseCard incident={incident} />
      <SuggestedFixes incident={incident} />
      <Button onClick={() => run(incident)}>{isRunning ? 'Running...' : 'Run triage'}</Button>
    </section>
  );
}
