/** Local daily inquiry measure — device-only, no account (ADR-0001). */

const USAGE_KEY = 'darshan.inquiryUsage';

export function localDateKey() {
  return new Date().toISOString().slice(0, 10);
}

function loadUsage() {
  try {
    const raw = localStorage.getItem(USAGE_KEY);
    if (!raw) return { date: localDateKey(), count: 0 };
    const parsed = JSON.parse(raw);
    if (parsed.date !== localDateKey()) return { date: localDateKey(), count: 0 };
    return { date: parsed.date, count: Number(parsed.count) || 0 };
  } catch {
    return { date: localDateKey(), count: 0 };
  }
}

function saveUsage(usage) {
  localStorage.setItem(USAGE_KEY, JSON.stringify(usage));
}

export function inquiriesUsedToday() {
  return loadUsage().count;
}

export function inquiriesRemaining(freeDaily) {
  if (freeDaily == null) return null;
  return Math.max(0, freeDaily - loadUsage().count);
}

export function canUseFreeInquiry(freeDaily) {
  if (freeDaily == null) return true;
  return loadUsage().count < freeDaily;
}

export function recordFreeInquiry() {
  const usage = loadUsage();
  usage.count += 1;
  saveUsage(usage);
  return usage.count;
}
