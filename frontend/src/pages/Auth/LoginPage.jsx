import { useState } from 'react';
import AuthLayout from '../../app/layouts/AuthLayout';
import Button from '../../shared/components/ui/Button';
import Input from '../../shared/components/ui/Input';
import { ROUTES } from '../../shared/constants/routes';
import { navigateTo } from '../../app/router';
import { useAuth } from '../../features/auth/hooks/useAuth';

export default function LoginPage() {
  const { login, saveSession } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setError('');
    try {
      saveSession(await login(form));
      navigateTo(ROUTES.DASHBOARD);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthLayout title="Welcome back" subtitle="Sign in to manage incidents, triage, response, and SLA risk.">
      <form className="auth-form" onSubmit={submit}>
        <Input
          id="login-email"
          label="Email"
          required
          type="email"
          value={form.email}
          onChange={(event) => setForm({ ...form, email: event.target.value })}
        />
        <Input
          id="login-password"
          label="Password"
          required
          type="password"
          value={form.password}
          onChange={(event) => setForm({ ...form, password: event.target.value })}
        />
        {error && <p className="form-error">{error}</p>}
        <Button disabled={isSubmitting} type="submit">{isSubmitting ? 'Signing in...' : 'Login'}</Button>
      </form>
      <button className="text-link" type="button" onClick={() => navigateTo(ROUTES.REGISTER)}>
        Create an account
      </button>
    </AuthLayout>
  );
}
