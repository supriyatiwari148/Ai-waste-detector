import { useState } from "react";
import UploadCard from "../components/UploadCard.jsx";
import ResultCard from "../components/ResultCard.jsx";
import Loader from "../components/Loader.jsx";
import { classifyImage } from "../services/api.js";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [error, setError] = useState("");

  async function analyze(file, previewUrl) {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const data = await classifyImage(file);
      setResult(data);
      setImageUrl(previewUrl);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <section className="hero">
        <div className="container">
          <h1>Sort your waste the smart way</h1>
          <p>Upload a photo of an item. Our AI suggests what kind of waste it is and how to dispose of it responsibly.</p>
        </div>
      </section>

      <div className="container stack">
        <UploadCard onAnalyze={analyze} loading={loading} />
        {loading && <Loader />}
        {error && <p className="alert error" role="alert">{error}</p>}
        {result && !loading && <ResultCard result={result} imageUrl={imageUrl} />}
      </div>
    </>
  );
}
