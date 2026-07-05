import { HOUR_THEMES } from './strings.js';

const STORAGE_HOUR = 'darshan.hourOverride';
const STORAGE_SKIP = 'darshan.skipThreshold';

/** Map local clock to hour theme (design-tokens.yaml). */
export function themeFromClock(date = new Date()) {
  const h = date.getHours();
  if (h >= 4 && h < 7) return 'pre_dawn';
  if (h >= 7 && h < 17) return 'day';
  if (h >= 17 && h < 20) return 'dusk';
  return 'night';
}

export function getHourOverride() {
  return localStorage.getItem(STORAGE_HOUR);
}

export function setHourOverride(theme) {
  if (!theme || theme === 'auto') {
    localStorage.removeItem(STORAGE_HOUR);
  } else if (HOUR_THEMES.includes(theme)) {
    localStorage.setItem(STORAGE_HOUR, theme);
  }
}

export function resolveHourTheme() {
  const override = getHourOverride();
  if (override && HOUR_THEMES.includes(override)) return override;
  return themeFromClock();
}

export function shouldSkipThreshold() {
  return localStorage.getItem(STORAGE_SKIP) === '1';
}

export function setSkipThreshold(forever = false) {
  if (forever) localStorage.setItem(STORAGE_SKIP, '1');
}

export function localDateKey(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export function breathDurationMs() {
  return prefersReducedMotion() ? 0 : 8000;
}
