/**
 * Base path for static assets ("" locally, "/aadi-yogi" on GitHub Pages).
 * Inferred from the app.js module URL so one build works everywhere.
 */
function detectBase() {
  try {
    const meta = document.querySelector('meta[name="darshan-base"]');
    if (meta && meta.content != null) {
      return String(meta.content).replace(/\/$/, '');
    }
    const script = document.querySelector('script[type="module"][src*="app.js"]');
    if (script?.src) {
      return new URL(script.src).pathname.replace(/\/static\/js\/app\.js$/, '');
    }
  } catch {
    /* ignore */
  }
  return '';
}

export const BASE = detectBase();

/** Absolute path under the app base, e.g. asset('/static/data/x.json'). */
export function asset(path) {
  const normalized = path.startsWith('/') ? path : `/${path}`;
  return `${BASE}${normalized}`;
}
