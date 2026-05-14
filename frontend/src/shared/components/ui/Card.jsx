import { cn } from '../../utils/cn';

export default function Card({ children, className, ...props }) {
  return (
    <section className={cn('card', className)} {...props}>
      {children}
    </section>
  );
}
