import { useState } from "react";
import { sendFeedback } from "../services/api.js";

// Text + style of the "recyclable?" badge
function recyclableBadge(value) {
  if (value === true) return ["badge yes", "♻️ Recyclable"];
  if (value === "limited") return ["badge maybe", "♻️ Only partly recyclable"];
  if (value === false) return ["badge no", "🚫 Not recyclable"];
  return ["badge maybe", "❓ Unknown - check your local rules"];
}

export default function ResultCard({ result, imageUrl }) {
  const [fb, setFb] = useState(null);
  const g = result.guidance;
  const [badgeClass, badgeText] = recyclableBadge(g.recyclable);

  async function feedback(correct) {
    try {
      await sendFeedback(result.id, correct);
      setFb("sent");
    } catch {
      setFb("error");
    }
  }

  return (
    <section className="card result-card" aria-live="polite">
      <div className="result-top">
        {imageUrl && <img src={imageUrl} alt="Analyzed item" className="result-img" />}
        <div>
          <p className="result-icon" aria-hidden="true">{g.icon}</p>
          <h2>{result.uncertain ? "Not sure about this one" : g.title}</h2>
          {!result.uncertain && g.waste_type && <p className="badge type">🗂️ {g.waste_type}</p>}
          <p><span className={badgeClass}>{badgeText}</span></p>
          <p className="confidence">
            Model confidence estimate: <strong>{Math.round(result.confidence * 100)}%</strong>
            <span className="small"> (an estimate, not guaranteed accuracy)</span>
          </p>
          {result.uncertain && <p className="alert warn">{result.uncertain_reason} Showing general advice instead.</p>}
        </div>
      </div>

      {g.warning && <div className="alert danger"><strong>⚠️ Safety:</strong> {g.warning}</div>}

      <div className="grid">
        <div><h3>Why this result</h3><p>{g.explanation}</p></div>
        <div><h3>How to dispose</h3><p>{g.disposal}</p></div>
        <div><h3>Recycling</h3><p>{g.recycling}</p></div>
        <div><h3>Where to take it</h3><p>{g.where}</p></div>
      </div>

      <h3>Model's closest guesses (not a verdict)</h3>
      <ul className="bars">
        {result.top_predictions.map((p) => (
          <li key={p.label}>
            <span className="bar-label">{p.label}</span>
            <span className="bar"><span style={{ width: `${Math.round(p.confidence * 100)}%` }} /></span>
            <span className="bar-pct">{Math.round(p.confidence * 100)}%</span>
          </li>
        ))}
      </ul>

      <p className="small">{g.local_note}</p>
      <p className="small">{result.disclaimer}</p>

      <div className="feedback">
        {fb === "sent" ? (
          <p>Thanks for the feedback! ✅</p>
        ) : (
          <>
            <span>Was this prediction correct?</span>
            <button className="btn ghost" onClick={() => feedback(true)}>👍 Yes</button>
            <button className="btn ghost" onClick={() => feedback(false)}>👎 No</button>
            {fb === "error" && <span className="alert error">Could not send feedback.</span>}
          </>
        )}
      </div>
    </section>
  );
}
