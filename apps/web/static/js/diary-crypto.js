/** Diary encryption — Web Crypto, user-derived key (RF-012). No server bytes. */

const SALT_KEY = 'darshan.diary.salt';
const VERIFY_KEY = 'darshan.diary.verify';
const SESSION_KEY = 'darshan.diary.session';
const ENC_KEY = 'darshan.diary.enc';

let unlockedKey = null;

function bufToB64(buf) {
  return btoa(String.fromCharCode(...new Uint8Array(buf)));
}

function b64ToBuf(b64) {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i += 1) bytes[i] = bin.charCodeAt(i);
  return bytes.buffer;
}

async function deriveKey(passphrase, saltBuf) {
  const enc = new TextEncoder();
  const baseKey = await crypto.subtle.importKey(
    'raw',
    enc.encode(passphrase),
    'PBKDF2',
    false,
    ['deriveKey'],
  );
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt: saltBuf, iterations: 120000, hash: 'SHA-256' },
    baseKey,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt'],
  );
}

async function fingerprint(passphrase, saltBuf) {
  const key = await deriveKey(passphrase, saltBuf);
  const raw = await crypto.subtle.exportKey('raw', key);
  return bufToB64(raw).slice(0, 24);
}

export function diaryConfigured() {
  return Boolean(localStorage.getItem(SALT_KEY) && localStorage.getItem(VERIFY_KEY));
}

export function diaryUnlocked() {
  return unlockedKey !== null;
}

export async function setupDiaryKey(passphrase) {
  if (passphrase.length < 8) throw new Error('passphrase too short');
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const key = await deriveKey(passphrase, salt);
  const verify = await fingerprint(passphrase, salt);
  localStorage.setItem(SALT_KEY, bufToB64(salt));
  localStorage.setItem(VERIFY_KEY, verify);
  unlockedKey = key;
  sessionStorage.setItem(SESSION_KEY, '1');
  await saveEncryptedDiary({ version: 1, entries: [] });
}

export async function unlockDiary(passphrase) {
  const salt = b64ToBuf(localStorage.getItem(SALT_KEY));
  const verify = await fingerprint(passphrase, salt);
  if (verify !== localStorage.getItem(VERIFY_KEY)) throw new Error('wrong passphrase');
  unlockedKey = await deriveKey(passphrase, salt);
  sessionStorage.setItem(SESSION_KEY, '1');
}

export function lockDiary() {
  unlockedKey = null;
  sessionStorage.removeItem(SESSION_KEY);
}

export async function tryRestoreSession(passphraseLoader) {
  if (!diaryConfigured() || !sessionStorage.getItem(SESSION_KEY)) return false;
  try {
    const pass = await passphraseLoader();
    if (!pass) return false;
    await unlockDiary(pass);
    return true;
  } catch {
    sessionStorage.removeItem(SESSION_KEY);
    return false;
  }
}

async function encryptJson(data) {
  if (!unlockedKey) throw new Error('diary locked');
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const enc = new TextEncoder();
  const cipher = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    unlockedKey,
    enc.encode(JSON.stringify(data)),
  );
  return `${bufToB64(iv)}.${bufToB64(cipher)}`;
}

async function decryptJson(blob) {
  if (!unlockedKey) throw new Error('diary locked');
  const [ivB64, cipherB64] = blob.split('.');
  const plain = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: b64ToBuf(ivB64) },
    unlockedKey,
    b64ToBuf(cipherB64),
  );
  return JSON.parse(new TextDecoder().decode(plain));
}

export async function loadEncryptedDiary() {
  const raw = localStorage.getItem(ENC_KEY);
  if (!raw) return { version: 1, entries: [] };
  return decryptJson(raw);
}

export async function saveEncryptedDiary(data) {
  localStorage.setItem(ENC_KEY, await encryptJson(data));
}
