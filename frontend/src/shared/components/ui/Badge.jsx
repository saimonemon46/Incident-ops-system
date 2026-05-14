import { cn } from '../../utils/cn';

export default function Badge({ children, tone = 'neutral' }) {
  return <span className={cn('badge', `badge-${tone}`)}>{children}</span>;
}
