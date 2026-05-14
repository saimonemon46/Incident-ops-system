import { ROUTES } from '../constants/routes';
import { useAuth } from '../../features/auth/hooks/useAuth';
import { navigateTo, useCurrentPath } from '../../app/router';
import Button from './ui/Button';

const navItems = [
  ['Dashboard', ROUTES.DASHBOARD],
  ['AI Triage', ROUTES.TRIAGE],
  ['Response', ROUTES.RESPONSE],
  ['SLA Watch', ROUTES.SLA],
];

export default function Sidebar() {
  const path = useCurrentPath();
  const { logout, user } = useAuth();

  return (
    <aside className="sidebar" aria-label="Primary navigation">
      <div className="brand-lockup">
        <span className="brand-mark">IO</span>
        <div>
          <strong>Incident Ops</strong>
          <span>{user?.role || 'Command Center'}</span>
        </div>
      </div>
      <nav className="nav-list">
        {navItems.map(([label, route]) => (
          <button className={path === route ? 'active' : ''} key={route} type="button" onClick={() => navigateTo(route)}>
            {label}
          </button>
        ))}
      </nav>
      <Button tone="ghost" onClick={logout}>Sign out</Button>
    </aside>
  );
}
