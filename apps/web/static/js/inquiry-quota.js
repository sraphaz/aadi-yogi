/** Device identity for anonymous inquiry measure — local only (ADR-0001). */

const DEVICE_KEY = 'darshan.deviceId';

export function getDeviceId() {
  let id = localStorage.getItem(DEVICE_KEY);
  if (!id) {
    id = typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : `dev-${Date.now()}`;
    localStorage.setItem(DEVICE_KEY, id);
  }
  return id;
}

export function deviceHeaders() {
  return { 'X-Darshan-Device': getDeviceId() };
}

export function inquiryFetchInit(body) {
  return {
    method: 'POST',
    headers: { ...deviceHeaders(), 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  };
}

export async function fetchInquiryQuota() {
  try {
    const res = await fetch('/inquiry/quota', { headers: deviceHeaders() });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

/** Scaffold grant — server rejects unless DARSHAN_ALLOW_DEV_CREDIT_GRANT is set. */
export async function grantDevCredits(amount = 10) {
  try {
    const res = await fetch('/inquiry/credits/grant', {
      method: 'POST',
      headers: { ...deviceHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount }),
    });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}
