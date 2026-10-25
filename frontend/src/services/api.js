// All backend calls live here, so URLs match the Flask routes in one place.
const BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

async function request(path, options) {
  let res;
  try {
    res = await fetch(`${BASE}${path}`, options);
  } catch {
    // fetch throws when the server is off, blocked by CORS, or the URL is wrong
    throw new Error("Cannot reach the server. Is the backend running on " + BASE + "?");
  }
  let data = null;
  try {
    data = await res.json();
  } catch {
    /* response was not JSON */
  }
  if (!res.ok || !data?.success) {
    throw new Error(data?.error || `Request failed (${res.status}).`);
  }
  return data;
}

export function classifyImage(file) {
  const form = new FormData(); // multipart upload; field name must be "image"
  form.append("image", file);
  return request("/api/classify", { method: "POST", body: form });
}

export const getHistory = () => request("/api/history");
export const clearHistory = () => request("/api/history", { method: "DELETE" });
export const sendFeedback = (id, correct) =>
  request("/api/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, correct }),
  });
