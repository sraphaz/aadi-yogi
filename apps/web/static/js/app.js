/**
 * Darshan PWA — Seed phase (threshold, court, word, library D0–D2, silence, i18n)
 */
import { STRINGS, LANGS, HOUR_THEMES } from './strings.js';
import {
  resolveHourTheme,
  setHourOverride,
  shouldSkipThreshold,
  setSkipThreshold,
  localDateKey,
  breathDurationMs,
} from './theme.js';

const state = {
  screen: 'threshold',
  lang: 'en',
  hour: 'day',
  depth: 0,
  libraryPassage: null,
  dailyBatch: null,
  silenceReturn: 'court',
  closing: false,
};

const root = document.getElementById('app');

function t() {
  return STRINGS[state.lang] || STRINGS.en;
}

function detectLang() {
  const saved = localStorage.getItem('darshan.lang');
  if (saved && LANGS.includes(saved)) return saved;
  const nav = (navigator.language || 'en').slice(0, 2);
  return LANGS.includes(nav) ? nav : 'en';
}

async function loadDailyWords() {
  if (state.dailyBatch) return state.dailyBatch;
  const res = await fetch('/static/data/daily-words.json');
  state.dailyBatch = await res.json();
  return state.dailyBatch;
}

function todayWord(batch) {
  const key = localDateKey();
  const entry = batch.entries[key];
  if (entry) return entry;
  const keys = Object.keys(batch.entries);
  return batch.entries[keys[keys.length - 1]];
}

function orderedCourtCards(cards) {
  const hour = state.hour;
  const copy = [...cards];
  const emphasize = (id) => {
    const idx = copy.findIndex((c) => c.id === id);
    if (idx > 0) {
      const [card] = copy.splice(idx, 1);
      copy.unshift(card);
    }
  };
  if (hour === 'pre_dawn' || hour === 'day') emphasize('word');
  if (hour === 'dusk') emphasize('practice');
  return copy;
}

function applyShellAttrs() {
  root.dataset.lang = state.lang;
  root.dataset.hour = state.hour;
  document.documentElement.lang = state.lang === 'pt' ? 'pt-BR' : state.lang;
}

function renderToolbar(showClosure = true) {
  const s = t();
  const langOpts = LANGS.map(
    (l) => `<option value="${l}" ${l === state.lang ? 'selected' : ''}>${l}</option>`,
  ).join('');
  const hourOverride = localStorage.getItem('darshan.hourOverride');
  const hourOpts = [
    `<option value="auto" ${!hourOverride ? 'selected' : ''}>${s.hourAuto}</option>`,
    ...HOUR_THEMES.map(
      (h) => `<option value="${h}" ${hourOverride === h ? 'selected' : ''}>${s.hourLines[h]}</option>`,
    ),
  ].join('');

  return `
    <div class="toolbar">
      <div class="wordmark">darshan</div>
      <div class="toolbar__actions">
        <label class="sr-only" for="lang-select">${s.langLabel}</label>
        <select id="lang-select" class="lang-select" aria-label="${s.langLabel}">${langOpts}</select>
        <label class="sr-only" for="hour-select">${s.hourLabel}</label>
        <select id="hour-select" class="hour-select" aria-label="${s.hourLabel}">${hourOpts}</select>
        ${showClosure ? `<button type="button" class="closure" data-action="close">${s.goGently} ${s.backCourt}</button>` : ''}
      </div>
    </div>`;
}

function renderDepthDial(entry, maxDepth = 2) {
  const s = t();
  const lang = state.lang;
  const names = s.depthNames.slice(0, maxDepth + 1);
  const chips = names
    .map(
      (name, i) =>
        `<button type="button" class="depth-chip ${i === state.depth ? 'is-active' : ''}" data-depth="${i}" aria-pressed="${i === state.depth}">${name}</button>`,
    )
    .join('');

  let body = '';
  if (state.depth === 0) {
    body = `<div class="depth-content__passage">${entry.word?.[lang] || entry.word?.en || ''}</div>
      <p class="depth-content__meta">${s.depthHints[0]}</p>`;
  } else if (state.depth === 1) {
    body = `<div class="depth-content__reading">${entry.d1?.[lang] || entry.d1?.en || ''}</div>`;
  } else {
    body = `<div class="depth-content__passage">${entry.d2?.[lang] || entry.d2?.en || ''}</div>
      <p class="depth-content__meta">${entry.citation?.[lang] || entry.citation?.en || ''}</p>
      <p class="depth-content__meta">${entry.passage_id || ''}</p>`;
  }

  return `
    <div class="depth-dial">
      <div class="depth-dial__nav" role="group" aria-label="depth">${chips}</div>
      <div class="depth-content">${body}</div>
    </div>`;
}

function renderLibraryDepth(passage) {
  const s = t();
  const lang = state.lang;
  const names = s.depthNames.slice(0, 3);
  const chips = names
    .map(
      (name, i) =>
        `<button type="button" class="depth-chip ${i === state.depth ? 'is-active' : ''}" data-depth="${i}">${name}</button>`,
    )
    .join('');

  let body = '';
  if (state.depth === 0) {
    body = `<div class="depth-content__passage">${passage.depths.d0[lang] || passage.depths.d0.en}</div>`;
  } else if (state.depth === 1) {
    body = `<div class="depth-content__reading">${passage.depths.d1[lang] || passage.depths.d1.en}</div>`;
  } else {
    body = `<div class="depth-content__passage">${passage.depths.d2[lang] || passage.depths.d2.en}</div>
      <p class="depth-content__meta">${passage.citation[lang] || passage.citation.en}</p>
      <p class="depth-content__meta">${passage.passage_id}</p>
      <p class="depth-content__original">${passage.original || ''}</p>`;
  }

  return `
    <div class="depth-dial">
      <div class="depth-dial__nav">${chips}</div>
      <div class="depth-content">${body}</div>
    </div>`;
}

async function renderThreshold() {
  const s = t();
  root.innerHTML = `
    <section class="threshold screen" aria-label="threshold">
      <div class="threshold__inner">
        <div class="breath-glyph" aria-hidden="true"></div>
        <p class="threshold__line">${s.thresholdLine}</p>
        <button type="button" class="btn-quiet" data-action="enter">${s.skipThreshold}</button>
        <button type="button" class="btn-quiet" data-action="enter-forever" style="margin-top:0.75rem;font-size:var(--type-meta)">${s.skipForever}</button>
      </div>
    </section>`;

  const duration = breathDurationMs();
  if (duration === 0) {
    setTimeout(() => goCourt(), 300);
    return;
  }
  state._thresholdTimer = setTimeout(() => goCourt(), duration);
}

function renderCourt() {
  const s = t();
  const cards = orderedCourtCards(s.courtCards)
    .map((card) => {
      const enabled = card.state === 'open';
      const emphasis = card.id === 'word' && (state.hour === 'pre_dawn' || state.hour === 'day') ? ' court-card--emphasis' : '';
      return `
        <button type="button" class="court-card${emphasis}" data-gesture="${card.id}" ${enabled ? '' : 'disabled'} aria-disabled="${!enabled}">
          <div class="court-card__name">${card.name}</div>
          <div class="court-card__desc">${card.desc}</div>
          ${card.state !== 'open' ? `<div class="court-card__state">${s.states[card.state]}</div>` : ''}
        </button>`;
    })
    .join('');

  root.innerHTML = `
    <section class="screen" aria-label="${s.court}">
      <div class="container">
        ${renderToolbar(false)}
        <div class="label">${s.court} · ${s.hourLines[state.hour]}</div>
        <div class="court-grid">${cards}</div>
        <button type="button" class="silence-link" data-action="silence">
          <span style="color:var(--halo)">◦</span> ${s.silenceRoom}
        </button>
        <p class="court-note">${s.courtNote}</p>
      </div>
      <button type="button" class="silence-glyph-fixed" data-action="silence" aria-label="${s.silenceRoom}">◦</button>
    </section>`;
}

async function renderWord() {
  const s = t();
  const batch = await loadDailyWords();
  const entry = todayWord(batch);
  const lang = state.lang;
  const wordText = entry.word?.[lang] || entry.word?.en || '';
  const citation = entry.citation?.[lang] || entry.citation?.en || '';

  root.innerHTML = `
    <section class="screen" aria-label="${s.wordLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${s.wordLabel} · ${localDateKey()}</div>
        <div class="sr-only" id="word-sr">${wordText}. ${citation}</div>
        <div class="word-display" aria-describedby="word-sr">
          <div class="word-display__text is-revealing" aria-hidden="true">${wordText}</div>
          <div class="word-display__citation">${citation}</div>
        </div>
        ${renderDepthDial(entry, 2)}
      </div>
    </section>`;
}

function renderLibraryShelf() {
  const s = t();
  const items = s.shelves
    .map(
      (sh) =>
        `<button type="button" class="shelf-item" data-shelf="${sh.id}">
          <div class="shelf-item__name">${sh.name}</div>
          <div class="shelf-item__line">${sh.line}</div>
        </button>`,
    )
    .join('');

  root.innerHTML = `
    <section class="screen" aria-label="${s.libraryLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${s.libraryLabel}</div>
        <p style="color:var(--ink-soft);font-size:var(--type-meta);max-width:var(--measure-reading);line-height:1.65">${s.libraryIntro}</p>
        <div class="shelf-list">${items}</div>
      </div>
    </section>`;
}

function renderLibraryReading() {
  const s = t();
  const passage = state.libraryPassage;
  root.innerHTML = `
    <section class="screen" aria-label="${s.libraryLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${passage.work[state.lang] || passage.work.en}</div>
        ${renderLibraryDepth(passage)}
      </div>
    </section>`;
}

function renderSilence() {
  const s = t();
  root.innerHTML = `
    <div class="silence-room" data-action="silence-exit" role="button" tabindex="0" aria-label="${s.silenceRoom}">
      <div class="silence-room__pulse" aria-hidden="true"></div>
    </div>`;
}

function renderFarewell() {
  const s = t();
  root.innerHTML = `<section class="farewell screen"><p>${s.farewell}</p></section>`;
}

function goCourt() {
  clearTimeout(state._thresholdTimer);
  state.screen = 'court';
  state.depth = 0;
  state.closing = false;
  renderCourt();
}

function navigate(screen) {
  state.screen = screen;
  state.depth = 0;
  if (screen === 'threshold') renderThreshold();
  else if (screen === 'court') renderCourt();
  else if (screen === 'word') renderWord();
  else if (screen === 'library') renderLibraryShelf();
  else if (screen === 'library-read') renderLibraryReading();
  else if (screen === 'silence') renderSilence();
  else if (screen === 'farewell') renderFarewell();
}

async function openLibraryPassage(id) {
  const res = await fetch(`/static/data/library/${id}.json`);
  state.libraryPassage = await res.json();
  state.depth = 0;
  state.screen = 'library-read';
  renderLibraryReading();
}

function closeSession() {
  state.closing = true;
  navigate('farewell');
  setTimeout(() => {
    state.closing = false;
    navigate('court');
  }, 2200);
}

root.addEventListener('click', async (e) => {
  const el = e.target.closest('[data-action], [data-gesture], [data-shelf], [data-depth]');
  if (!el) return;

  if (el.dataset.action === 'enter') {
    goCourt();
    return;
  }
  if (el.dataset.action === 'enter-forever') {
    setSkipThreshold(true);
    goCourt();
    return;
  }
  if (el.dataset.action === 'silence' || el.dataset.action === 'silence-exit') {
    state.silenceReturn = state.screen === 'court' ? 'court' : state.screen;
    navigate('silence');
    if (el.dataset.action === 'silence-exit') navigate(state.silenceReturn);
    return;
  }
  if (el.dataset.action === 'close') {
    closeSession();
    return;
  }
  if (el.dataset.gesture === 'word') navigate('word');
  if (el.dataset.gesture === 'library') navigate('library');
  if (el.dataset.shelf) openLibraryPassage(el.dataset.shelf === 'gita' ? 'gita-ii-47' : el.dataset.shelf);
  if (el.dataset.depth !== undefined) {
    state.depth = Number(el.dataset.depth);
    if (state.screen === 'word') renderWord();
    if (state.screen === 'library-read') renderLibraryReading();
  }
});

root.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && state.screen !== 'court' && state.screen !== 'threshold' && !state.closing) {
    navigate('court');
  }
  if (state.screen === 'silence' && (e.key === 'Enter' || e.key === ' ')) {
    navigate(state.silenceReturn);
  }
});

root.addEventListener('change', (e) => {
  if (e.target.id === 'lang-select') {
    state.lang = e.target.value;
    localStorage.setItem('darshan.lang', state.lang);
    applyShellAttrs();
    navigate(state.screen);
  }
  if (e.target.id === 'hour-select') {
    const val = e.target.value;
    setHourOverride(val === 'auto' ? null : val);
    state.hour = resolveHourTheme();
    applyShellAttrs();
    navigate(state.screen);
  }
});

async function init() {
  state.lang = detectLang();
  state.hour = resolveHourTheme();
  applyShellAttrs();

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }

  await loadDailyWords();

  if (shouldSkipThreshold()) goCourt();
  else renderThreshold();
}

init();
