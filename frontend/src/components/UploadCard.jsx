import { useEffect, useRef, useState } from "react";

const ALLOWED = ["image/jpeg", "image/png"];
const MAX_MB = 5; // keep in sync with MAX_UPLOAD_MB in backend/.env

export default function UploadCard({ onAnalyze, loading }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState("");
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef(null);

  // Free the temporary preview URL when it changes or the component unmounts.
  useEffect(() => () => preview && URL.revokeObjectURL(preview), [preview]);

  function choose(f) {
    setError("");
    if (!f) return;
    if (!ALLOWED.includes(f.type)) return setError("Please choose a JPG, JPEG or PNG image.");
    if (f.size > MAX_MB * 1024 * 1024) return setError(`File is too large. Maximum is ${MAX_MB} MB.`);
    setFile(f);
    setPreview(URL.createObjectURL(f));
  }

  function onDrop(e) {
    e.preventDefault();
    setDragging(false);
    choose(e.dataTransfer.files?.[0]);
  }

  return (
    <section className="card upload-card">
      <div
        className={dragging ? "dropzone dragging" : "dropzone"}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && inputRef.current?.click()}
      >
        {preview ? (
          <img src={preview} alt="Selected waste item preview" className="preview" />
        ) : (
          <>
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
              <path d="M12 16V4m0 0L7 9m5-5 5 5" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3" strokeLinecap="round" />
            </svg>
            <p><strong>Drag & drop</strong> an image here, or click to browse</p>
            <p className="small">JPG, JPEG or PNG · up to {MAX_MB} MB <p className="small">For best results, photograph one item at a time on a plain background. Piles of mixed waste can't be analysed.</p></p>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept=".jpg,.jpeg,.png,image/jpeg,image/png"
          hidden
          onChange={(e) => choose(e.target.files?.[0])}
        />
      </div>

      {error && <p className="alert error" role="alert">{error}</p>}

      <div className="actions">
        <button className="btn primary" disabled={!file || loading} onClick={() => onAnalyze(file, preview)}>
          {loading ? "Analyzing..." : "Analyze Waste"}
        </button>
        {file && !loading && (
          <button className="btn ghost" onClick={() => { setFile(null); setPreview(null); }}>
            Remove
          </button>
        )}
      </div>
    </section>
  );
}
