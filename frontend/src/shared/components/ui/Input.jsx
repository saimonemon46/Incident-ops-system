export default function Input({ label, id, as = 'input', ...props }) {
  const Component = as;

  return (
    <label className="field" htmlFor={id}>
      <span>{label}</span>
      <Component id={id} {...props} />
    </label>
  );
}
