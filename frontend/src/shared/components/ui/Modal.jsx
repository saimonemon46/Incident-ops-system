import Button from './Button';

export default function Modal({ children, isOpen, onClose, title }) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-backdrop" role="presentation">
      <section className="modal" role="dialog" aria-modal="true" aria-label={title}>
        <header className="modal-header">
          <h2>{title}</h2>
          <Button aria-label="Close modal" tone="ghost" onClick={onClose}>
            X
          </Button>
        </header>
        {children}
      </section>
    </div>
  );
}
