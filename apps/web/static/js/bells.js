/** Opt-in dawn/dusk bells — max two lines daily, off by default (RF-013). */

import { skySnapshot } from './ephemeris.js';
import { recordPresence } from './presence-metrics.js';

const KEY = 'darshan.bells';
const FIRED_KEY = 'darshan.bells.fired';

const DEFAULT = {
  enabled: false,
  dawn: true,
  dusk: true,
};

export function loadBellSettings() {
  try {
    return { ...DEFAULT, ...JSON.parse(localStorage.getItem(KEY) || '{}') };
  } catch {
    return { ...DEFAULT };
  }
}

export function saveBellSettings(settings) {
  localStorage.setItem(KEY, JSON.stringify(settings));
}

function todayKey() {
  return new Date().toISOString().slice(0, 10);
}

function firedToday() {
  try {
    const all = JSON.parse(localStorage.getItem(FIRED_KEY) || '{}');
    return all[todayKey()] || { dawn: false, dusk: false };
  } catch {
    return { dawn: false, dusk: false };
  }
}

function markFired(slot) {
  try {
    const all = JSON.parse(localStorage.getItem(FIRED_KEY) || '{}');
    const day = all[todayKey()] || { dawn: false, dusk: false };
    day[slot] = true;
    all[todayKey()] = day;
    localStorage.setItem(FIRED_KEY, JSON.stringify(all));
  } catch {
    localStorage.setItem(FIRED_KEY, JSON.stringify({ [todayKey()]: { [slot]: true } }));
  }
}

function minutesNow() {
  const d = new Date();
  return d.getHours() * 60 + d.getMinutes();
}

export async function requestBellPermission() {
  if (!('Notification' in window)) return false;
  if (Notification.permission === 'granted') return true;
  if (Notification.permission === 'denied') return false;
  const res = await Notification.requestPermission();
  return res === 'granted';
}

function showBell(title, body) {
  if (Notification.permission !== 'granted') return;
  const n = new Notification(title, { body, tag: 'darshan-bell', silent: false });
  n.onclick = () => {
    window.focus();
    n.close();
  };
  recordPresence('bell');
}

export function maybeRingBells(lines) {
  const settings = loadBellSettings();
  if (!settings.enabled || Notification.permission !== 'granted') return;

  const fired = firedToday();
  const snap = skySnapshot();
  const now = minutesNow();
  const dawnTarget = snap.times.brahmamuhurta;
  const duskTarget = snap.times.sunset;

  if (settings.dawn && !fired.dawn && Math.abs(now - dawnTarget) <= 8) {
    showBell('darshan', lines.dawn);
    markFired('dawn');
  }
  if (settings.dusk && !fired.dusk && Math.abs(now - duskTarget) <= 8) {
    showBell('darshan', lines.dusk);
    markFired('dusk');
  }
}

export function scheduleBellChecks(lines) {
  maybeRingBells(lines);
  window.setInterval(() => maybeRingBells(lines), 60000);
}
