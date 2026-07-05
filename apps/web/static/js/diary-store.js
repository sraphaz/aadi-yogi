/** Inner diary entries — encrypted local-first (RF-012). */

import { diaryUnlocked, loadEncryptedDiary, saveEncryptedDiary } from './diary-crypto.js';

export async function listEntries() {
  if (!diaryUnlocked()) return [];
  const data = await loadEncryptedDiary();
  return data.entries || [];
}

export async function appendEntry({ body, kind = 'free', dateKey }) {
  if (!diaryUnlocked()) throw new Error('diary locked');
  const data = await loadEncryptedDiary();
  const entry = {
    id: crypto.randomUUID(),
    dateKey: dateKey || new Date().toISOString().slice(0, 10),
    createdAt: new Date().toISOString(),
    kind,
    body: body.trim(),
    title: body.trim().split('\n')[0].slice(0, 80),
  };
  data.entries = [entry, ...(data.entries || [])].slice(0, 120);
  await saveEncryptedDiary(data);
  return entry;
}

export async function entriesForDate(dateKey) {
  return (await listEntries()).filter((e) => e.dateKey === dateKey);
}
