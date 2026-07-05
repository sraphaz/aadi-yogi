/** On-device presence metrics only — no engagement telemetry (RF-015). */

const KEY = 'darshan.presence.v1';

const DEFAULT = {
  closures: 0,
  depthOpens: 0,
  silences: 0,
  witnessInvites: 0,
  bellsShown: 0,
};

export function loadPresence() {
  try {
    return { ...DEFAULT, ...JSON.parse(localStorage.getItem(KEY) || '{}') };
  } catch {
    return { ...DEFAULT };
  }
}

function savePresence(data) {
  localStorage.setItem(KEY, JSON.stringify(data));
}

export function recordPresence(event) {
  const data = loadPresence();
  if (event === 'closure') data.closures += 1;
  if (event === 'depth') data.depthOpens += 1;
  if (event === 'silence') data.silences += 1;
  if (event === 'witness') data.witnessInvites += 1;
  if (event === 'bell') data.bellsShown += 1;
  savePresence(data);
}

export function presenceSummary() {
  const p = loadPresence();
  return {
    closures: p.closures,
    depthOpens: p.depthOpens,
    silences: p.silences,
    witnessInvites: p.witnessInvites,
    bellsShown: p.bellsShown,
  };
}
