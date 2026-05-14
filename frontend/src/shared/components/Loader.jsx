export default function Loader({ label = 'Loading...' }) {
  return <p className="loader" role="status">{label}</p>;
}
