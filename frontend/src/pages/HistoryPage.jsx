import { useEffect, useState } from "react";
import { getHistory, clearHistory } from "../services/api.js";

export default function HistoryPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    try {
      setItems((await getHistory()).history);
      setError("");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => { load(); }, []);

  async function clearAll() {
    if (!window.confirm("Delete all history?")) return;
    try {
      await clearHistory();
      setItems([]);
    } catch (e) {
      setError(e.message);
    }
  }

  const fbText = (v) => (v === 1 ? "👍 correct" : v === 0 ? "👎 wrong" : "—");

  return (
    <div className="container stack page">
      <div className="row">
        <h1>Analysis history</h1>
        {items.length > 0 && <button className="btn ghost" onClick={clearAll}>Clear history</button>}
      </div>
      <p className="small">Only text results are saved. Your photos are never stored.</p>
      {loading && <p>Loading...</p>}
      {error && <p className="alert error">{error}</p>}
      {!loading && !error && items.length === 0 && <p>No analyses yet.</p>}
      {items.length > 0 && (
        <div className="card table-wrap">
          <table>
            <thead><tr><th>Time (UTC)</th><th>Result</th><th>Confidence</th><th>Feedback</th></tr></thead>
            <tbody>
              {items.map((i) => (
                <tr key={i.id}>
                  <td>{i.created_at}</td>
                  <td>{i.uncertain ? "Not sure" : i.category}</td>
                  <td>{Math.round(i.confidence * 100)}%</td>
                  <td>{fbText(i.feedback)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
