import { useEffect, useState } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { AuthProvider } from '../../features/auth/store/authStore';
import { IncidentProvider } from '../../features/incidents/store/incidentStore';
import { useAuth } from '../../features/auth/hooks/useAuth';
import Modal from '../../shared/components/ui/Modal';
import Loader from '../../shared/components/Loader';
import CreateIncidentForm from '../../features/incidents/components/CreateIncidentForm';
import { ROUTES } from '../../shared/constants/routes';
import DashboardPage from '../../pages/Dashboard/DashboardPage';
import AITriagePage from '../../pages/AI_Triage/AITriagePage';
import ResponsePage from '../../pages/Response/ResponsePage';
import SLAPage from '../../pages/SLA/SLAPage';
import LoginPage from '../../pages/Auth/LoginPage';
import RegisterPage from '../../pages/Auth/RegisterPage';

function readHashPath() {
  return window.location.hash.replace(/^#/, '') || ROUTES.DASHBOARD;
}

export function navigateTo(path) {
  window.location.hash = path;
}

export function useCurrentPath() {
  const [path, setPath] = useState(readHashPath);

  useEffect(() => {
    function handleHashChange() {
      setPath(readHashPath());
    }

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  return path;
}

function ProtectedApp() {
  const path = useCurrentPath();
  const { isAuthenticated, isBooting } = useAuth();
  const [isCreateOpen, setIsCreateOpen] = useState(false);

  useEffect(() => {
    if (!isBooting && !isAuthenticated && path !== ROUTES.REGISTER) {
      navigateTo(ROUTES.LOGIN);
    }
  }, [isAuthenticated, isBooting, path]);

  if (isBooting) {
    return <Loader label="Checking session..." />;
  }

  if (!isAuthenticated) {
    return path === ROUTES.REGISTER ? <RegisterPage /> : <LoginPage />;
  }

  const pages = {
    [ROUTES.DASHBOARD]: <DashboardPage />,
    [ROUTES.TRIAGE]: <AITriagePage />,
    [ROUTES.RESPONSE]: <ResponsePage />,
    [ROUTES.SLA]: <SLAPage />,
  };

  return (
    <IncidentProvider>
      <DashboardLayout onCreateIncident={() => setIsCreateOpen(true)}>
        {pages[path] || <DashboardPage />}
      </DashboardLayout>
      <Modal isOpen={isCreateOpen} title="Create incident" onClose={() => setIsCreateOpen(false)}>
        <CreateIncidentForm onCreated={() => setIsCreateOpen(false)} />
      </Modal>
    </IncidentProvider>
  );
}

export default function AppRouter() {
  return (
    <AuthProvider>
      <ProtectedApp />
    </AuthProvider>
  );
}
