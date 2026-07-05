/** Local ephemeris — rhythm not fate (RF-030, RF-031). No network, no natal data. */

const SYNODIC_MONTH = 29.530588853;
const RITU_NAMES = ['vasanta', 'grishma', 'varsha', 'sharad', 'hemanta', 'shishira'];

export function julianDay(date = new Date()) {
  return date.getTime() / 86400000 + 2440587.5;
}

export function moonAgeDays(date = new Date()) {
  const jd = julianDay(date);
  let age = (jd - 2451549.5) % SYNODIC_MONTH;
  if (age < 0) age += SYNODIC_MONTH;
  return age;
}

export function moonIllumination(date = new Date()) {
  const age = moonAgeDays(date);
  return (1 - Math.cos((2 * Math.PI * age) / SYNODIC_MONTH)) / 2;
}

export function moonPhaseName(date = new Date()) {
  const age = moonAgeDays(date);
  if (age < 1.85) return 'new moon';
  if (age < 7.38) return 'waxing crescent';
  if (age < 9.23) return 'first quarter';
  if (age < 14.77) return 'waxing gibbous';
  if (age < 16.61) return 'full moon';
  if (age < 22.15) return 'waning gibbous';
  if (age < 23.99) return 'last quarter';
  if (age < 27.68) return 'waning crescent';
  return 'new moon';
}

export function approximateTithi(date = new Date()) {
  return Math.floor(moonAgeDays(date)) + 1;
}

/** Simplified sun times (NOAA-style), minutes from midnight local. */
export function sunTimes(date, lat, lon) {
  const rad = Math.PI / 180;
  const d = julianDay(date) - 2451545;
  const g = (357.529 + 0.98560028 * d) % 360;
  const q = (280.459 + 0.98564736 * d) % 360;
  const l = (q + 1.915 * Math.sin(g * rad) + 0.02 * Math.sin(2 * g * rad) + 180) % 360;
  const e = 23.439 - 0.00000036 * d;
  const ra = Math.atan2(Math.cos(e * rad) * Math.sin(l * rad), Math.cos(l * rad)) / rad;
  const dec = Math.asin(Math.sin(e * rad) * Math.sin(l * rad)) / rad;
  const jnoon = 720 - 4 * lon - eqTime(ra, l, e, rad);
  const ha = Math.acos(
    Math.max(-1, Math.min(1, (Math.cos(90.833 * rad) - Math.sin(lat * rad) * Math.sin(dec * rad)) / (Math.cos(lat * rad) * Math.cos(dec * rad)))),
  ) / rad;
  const sunrise = jnoon - ha * 4;
  const sunset = jnoon + ha * 4;
  const brahmamuhurta = sunrise - 96;
  return {
    sunrise: clampMinutes(sunrise),
    sunset: clampMinutes(sunset),
    solarNoon: clampMinutes(jnoon),
    brahmamuhurta: clampMinutes(brahmamuhurta),
  };
}

function eqTime(ra, l, e, rad) {
  return 4 * (ra - 0.0057183 - Math.atan2(Math.tan(l * rad), Math.cos(e * rad)) / rad);
}

function clampMinutes(m) {
  let v = m;
  while (v < 0) v += 1440;
  while (v >= 1440) v -= 1440;
  return v;
}

export function formatMinutes(m) {
  const h = Math.floor(m / 60);
  const min = Math.round(m % 60);
  return `${String(h).padStart(2, '0')}:${String(min).padStart(2, '0')}`;
}

export function currentRitu(date = new Date(), hemisphere = 'south') {
  const month = date.getMonth();
  const idx = hemisphere === 'south' ? (month + 9) % 12 : month;
  return RITU_NAMES[Math.floor(idx / 2) % 6];
}

export function rhythmCopy(hourTheme) {
  const lines = {
    pre_dawn: 'the still hour — good ground for silence',
    day: 'the working hours — the field is open',
    dusk: 'the look-back hour — gather the day',
    night: 'the near-silence — let it settle',
  };
  return lines[hourTheme] || lines.day;
}

export function defaultLocation() {
  return { lat: -23.55, lon: -46.63, label: 'são paulo', hemisphere: 'south' };
}

export function loadLocation() {
  try {
    const raw = localStorage.getItem('darshan.location');
    if (raw) return { ...defaultLocation(), ...JSON.parse(raw) };
  } catch {
    /* ignore */
  }
  return defaultLocation();
}

export function saveLocation(loc) {
  localStorage.setItem('darshan.location', JSON.stringify(loc));
}

export async function requestDeviceLocation() {
  if (!navigator.geolocation) return null;
  return new Promise((resolve) => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const loc = {
          lat: pos.coords.latitude,
          lon: pos.coords.longitude,
          label: 'here',
          hemisphere: pos.coords.latitude >= 0 ? 'north' : 'south',
        };
        saveLocation(loc);
        resolve(loc);
      },
      () => resolve(null),
      { maximumAge: 600000, timeout: 8000 },
    );
  });
}

export function skySnapshot(date = new Date(), loc = loadLocation()) {
  const times = sunTimes(date, loc.lat, loc.lon);
  return {
    phase: moonPhaseName(date),
    illumination: moonIllumination(date),
    tithi: approximateTithi(date),
    ritu: currentRitu(date, loc.hemisphere),
    times,
    rhythm: rhythmCopy(
      date.getHours() >= 4 && date.getHours() < 7
        ? 'pre_dawn'
        : date.getHours() >= 17 && date.getHours() < 20
          ? 'dusk'
          : date.getHours() >= 20 || date.getHours() < 4
            ? 'night'
            : 'day',
    ),
    locationLabel: loc.label,
  };
}
