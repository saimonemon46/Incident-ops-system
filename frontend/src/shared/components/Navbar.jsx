import Button from './ui/Button';

export default function Navbar({ onCreateIncident }) {
  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">Live response</p>
        <h1>Incident Dashboard</h1>
      </div>
      <Button onClick={onCreateIncident}>Create incident</Button>
    </header>
  );
}
