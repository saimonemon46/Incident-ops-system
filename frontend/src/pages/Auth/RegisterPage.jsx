import { useState } from 'react';
import AuthLayout from '../../app/layouts/AuthLayout';
import Button from '../../shared/components/ui/Button';
import Input from '../../shared/components/ui/Input';
import { ROUTES } from '../../shared/constants/routes';
import { navigateTo } from '../../app/router';
import { useAuth } from '../../features/auth/hooks/useAuth';

export default function RegisterPage() {
  const { register, saveSession } = useAuth();
  const [form, setForm] = useState({ email: '', username: '', password: '', role: 'ENGINEER' });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setError('');
    try {
      saveSession(await register(form));
      navigateTo(ROUTES.DASHBOARD);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthLayout title="Create account" subtitle="Register a responder account and enter the protected workspace.">
      <form className="auth-form" onSubmit={submit}>
        <Input
          id="register-email"
          label="Email"
          required
          type="email"
          value={form.email}
          onChange={(event) => setForm({ ...form, email: event.target.value })}
        />
        <Input
          id="register-username"
          label="Username"
          minLength="3"
          required
          value={form.username}
          onChange={(event) => setForm({ ...form, username: event.target.value })}
        />
        <Input
          id="register-password"
          label="Password"
          minLength="8"
          required
          type="password"
          value={form.password}
          onChange={(event) => setForm({ ...form, password: event.target.value })}
        />
        <label className="field" htmlFor="register-role">
          <span>Role</span>
          <select id="register-role" value={form.role} onChange={(event) => setForm({ ...form, role: event.target.value })}>
            <option value="ENGINEER">Engineer</option>
            <option value="MANAGER">Manager</option>
            <option value="ADMIN">Admin</option>
          </select>
        </label>
        {error && <p className="form-error">{error}</p>}
        <Button disabled={isSubmitting} type="submit">{isSubmitting ? 'Creating...' : 'Register'}</Button>
      </form>
      <button className="text-link" type="button" onClick={() => navigateTo(ROUTES.LOGIN)}>
        Back to login
      </button>
    </AuthLayout>
  );
}
