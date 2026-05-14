import { cn } from '../../utils/cn';

export default function Button({ children, className, tone = 'primary', ...props }) {
  return (
    <button className={cn('button', `button-${tone}`, className)} type="button" {...props}>
      {children}
    </button>
  );
}
