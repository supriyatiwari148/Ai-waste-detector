export default function Loader({ text = "Analyzing your image..." }) {
  return (
    <div className="loader" role="status" aria-live="polite">
      <div className="spinner" />
      <p>{text}</p>
      <p className="small">The first request can take a minute while the model loads.</p>
    </div>
  );
}
