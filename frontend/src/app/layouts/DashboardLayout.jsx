import Navbar from '../../shared/components/Navbar';
import Sidebar from '../../shared/components/Sidebar';

export default function DashboardLayout({ children, onCreateIncident }) {
  return (
    <main className="dashboard-shell">
      <Sidebar />
      <section className="workspace">
        <Navbar onCreateIncident={onCreateIncident} />
        {children}
      </section>
    </main>
  );
}
