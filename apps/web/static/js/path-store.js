/** Local-first path state — no analytics, no progress percentages (Path phase). */

const KEYS = {
  posture: 'darshan.posture',
  mapStep: 'darshan.mapStep',
  rhythm: 'darshan.rhythm',
  innerSky: 'darshan.innerSky',
  offering: 'darshan.offering',
  lookback: 'darshan.lookback',
};

export const POSTURES = ['touched', 'seeking', 'practicing', 'integrating'];

export function loadPosture() {
  return localStorage.getItem(KEYS.posture) || 'seeking';
}

export function savePosture(id) {
  if (POSTURES.includes(id)) localStorage.setItem(KEYS.posture, id);
}

export function loadMapStep(mapId) {
  return Number(localStorage.getItem(`${KEYS.mapStep}.${mapId}`) || '0');
}

export function saveMapStep(mapId, step) {
  localStorage.setItem(`${KEYS.mapStep}.${mapId}`, String(Math.max(0, step)));
}

export function loadRhythm() {
  try {
    return {
      word: true,
      offering: true,
      remembrance: false,
      lookback: true,
      silence: true,
      bindSky: false,
      ...JSON.parse(localStorage.getItem(KEYS.rhythm) || '{}'),
    };
  } catch {
    return { word: true, offering: true, remembrance: false, lookback: true, silence: true, bindSky: false };
  }
}

export function saveRhythm(settings) {
  localStorage.setItem(KEYS.rhythm, JSON.stringify(settings));
}

export function loadInnerSky() {
  try {
    return JSON.parse(localStorage.getItem(KEYS.innerSky) || '{}');
  } catch {
    return {};
  }
}

export function saveInnerSky(marks) {
  localStorage.setItem(KEYS.innerSky, JSON.stringify(marks));
}

export function loadOffering(dateKey) {
  try {
    const all = JSON.parse(localStorage.getItem(KEYS.offering) || '{}');
    return all[dateKey] || '';
  } catch {
    return '';
  }
}

export function saveOffering(dateKey, text) {
  try {
    const all = JSON.parse(localStorage.getItem(KEYS.offering) || '{}');
    all[dateKey] = text;
    localStorage.setItem(KEYS.offering, JSON.stringify(all));
  } catch {
    localStorage.setItem(KEYS.offering, JSON.stringify({ [dateKey]: text }));
  }
}

export function loadLookback(dateKey) {
  try {
    const all = JSON.parse(localStorage.getItem(KEYS.lookback) || '{}');
    return all[dateKey] || ['', '', ''];
  } catch {
    return ['', '', ''];
  }
}

export function saveLookback(dateKey, answers) {
  try {
    const all = JSON.parse(localStorage.getItem(KEYS.lookback) || '{}');
    all[dateKey] = answers;
    localStorage.setItem(KEYS.lookback, JSON.stringify(all));
  } catch {
    localStorage.setItem(KEYS.lookback, JSON.stringify({ [dateKey]: answers }));
  }
}
