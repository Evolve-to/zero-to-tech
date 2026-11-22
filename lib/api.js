// The dev server and FastAPI run on separate ports. In production, Nginx
// serves the frontend and proxies same-origin /api requests to FastAPI.
const API_BASE_URL =
  process.env.NODE_ENV === "development" ? "http://localhost:8000" : "";

export function apiUrl(path) {
  return `${API_BASE_URL}${path}`;
}
