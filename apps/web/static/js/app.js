/**
 * Darshan PWA — Seed + Voice + Path (threshold, court, word, library, inquiry, maps, practice, sky)
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
import {
  skySnapshot,
  formatMinutes,
  requestDeviceLocation,
  loadLocation,
} from './ephemeris.js';
import {
  POSTURES,
  loadPosture,
  savePosture,
  loadMapStep,
  saveMapStep,
  loadRhythm,
  saveRhythm,
  loadInnerSky,
  saveInnerSky,
  loadOffering,
  saveOffering,
  loadLookback,
  saveLookback,
} from './path-store.js';

const state = {
  screen: 'threshold',
  lang: 'en',
  hour: 'day',
  depth: 0,
  libraryPassage: null,
  dailyBatch: null,
  silenceReturn: 'court',
  closing: false,
  inquiryDoor: null,
  inquiryQuestion: '',
  contemplation: null,
  livingMap: null,
  mapData: null,
};

const root = document.getElementById('app');

function t() {
  return { ...STRINGS.en, ...(STRINGS[state.lang] || {}) };
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
      const emphasis =
        (card.id === 'word' && (state.hour === 'pre_dawn' || state.hour === 'day')) ||
        (card.id === 'practice' && state.hour === 'dusk')
          ? ' court-card--emphasis'
          : '';
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

function pickLang(obj) {
  if (!obj) return '';
  return obj[state.lang] || obj.en || '';
}

async function loadLivingMap(id) {
  const res = await fetch(`/static/data/living-maps/${id}.json`);
  return res.json();
}

function renderPostureChips(active) {
  const s = t();
  return POSTURES.map(
    (p) =>
      `<button type="button" class="door-chip ${active === p ? 'is-active' : ''}" data-posture="${p}">${s.postures[p]}</button>`,
  ).join('');
}

function renderMapsList() {
  const s = t();
  root.innerHTML = `
    <section class="screen" aria-label="${s.mapsLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${s.mapsLabel}</div>
        <p class="path-intro">${s.mapsIntro}</p>
        <div class="shelf-list">
          <button type="button" class="shelf-item" data-map="aspiration-path">
            <div class="shelf-item__name">${pickLang({ en: 'aspiration path', pt: 'caminho da aspiração' })}</div>
            <div class="shelf-item__line">${s.stationNote}</div>
          </button>
        </div>
      </div>
    </section>`;
}

async function renderMapJourney() {
  const s = t();
  const map = state.mapData;
  if (!map) return navigate('maps');

  const lang = state.lang;
  const step = loadMapStep(map.id);
  const posture = loadPosture();
  const stations = map.stations || [];
  const atEnd = step >= stations.length;
  const stationText = atEnd
    ? pickLang({ en: 'the crossing rests here for now.', pt: 'a travessia repousa aqui por agora.' })
    : stations[step][lang] || stations[step].en;

  root.innerHTML = `
    <section class="screen" aria-label="${pickLang(map.name)}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${pickLang(map.name)}</div>
        <p class="path-intro">${map.start[lang] || map.start.en}</p>
        <div class="label label--soft">${s.postureLabel}</div>
        <div class="door-grid" role="group">${renderPostureChips(posture)}</div>
        <div class="map-station">
          <div class="map-station__glyph" aria-hidden="true">◦</div>
          <p class="map-station__text">${stationText}</p>
          <p class="path-note">${map.caution[lang] || map.caution.en}</p>
          <p class="path-note path-note--muted">${s.stationNote}</p>
        </div>
        <div class="path-actions">
          ${atEnd ? '' : `<button type="button" class="btn-quiet" data-action="map-next">${s.stationNext}</button>`}
          <button type="button" class="btn-quiet" data-action="map-stay">${s.stationStay}</button>
        </div>
        <p class="path-meta">${map.sources}</p>
      </div>
    </section>`;
}

function renderPractice() {
  const s = t();
  const items = [
    { id: 'practice-silence', name: s.practiceSilence },
    { id: 'offering', name: s.practiceOffering },
    { id: 'lookback', name: s.practiceLookback },
    { id: 'rhythm', name: s.practiceRhythm },
  ]
    .map(
      (item) =>
        `<button type="button" class="shelf-item" data-gesture="${item.id}">
          <div class="shelf-item__name">${item.name}</div>
        </button>`,
    )
    .join('');

  root.innerHTML = `
    <section class="screen" aria-label="${s.practiceLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${s.practiceLabel}</div>
        <p class="path-intro">${s.practiceIntro}</p>
        <div class="shelf-list">${items}</div>
      </div>
    </section>`;
}

function renderOffering() {
  const s = t();
  const key = localDateKey();
  const text = loadOffering(key);

  root.innerHTML = `
    <section class="screen" aria-label="${s.offeringLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${s.offeringLabel} · ${key}</div>
        <p class="path-intro">${s.offeringIntro}</p>
        <form class="inquiry-form" data-action="offering-save">
          <label class="sr-only" for="offering-field">${s.offeringPlaceholder}</label>
          <textarea id="offering-field" class="inquiry-field" rows="5" maxlength="2000" placeholder="${s.offeringPlaceholder}">${text}</textarea>
          <button type="submit" class="btn-quiet inquiry-submit">${s.offeringSave}</button>
        </form>
      </div>
    </section>`;
}

function renderLookback() {
  const s = t();
  const key = localDateKey();
  const answers = loadLookback(key);
  const fields = s.lookbackQuestions
    .map(
      (q, i) =>
        `<label class="lookback-field">
          <span class="lookback-field__q">${q}</span>
          <textarea class="inquiry-field" rows="3" maxlength="1200" data-lookback-idx="${i}">${answers[i] || ''}</textarea>
        </label>`,
    )
    .join('');

  root.innerHTML = `
    <section class="screen" aria-label="${s.lookbackLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${s.lookbackLabel} · ${key}</div>
        <p class="path-intro">${s.lookbackIntro}</p>
        <form class="inquiry-form" data-action="lookback-save">${fields}
          <button type="submit" class="btn-quiet inquiry-submit">${s.lookbackSave}</button>
        </form>
      </div>
    </section>`;
}

function renderRhythm() {
  const s = t();
  const rhythm = loadRhythm();
  const joints = Object.entries(s.rhythmJoints)
    .map(
      ([key, label]) =>
        `<label class="rhythm-row">
          <input type="checkbox" data-rhythm="${key}" ${rhythm[key] ? 'checked' : ''} />
          <span>${label}</span>
        </label>`,
    )
    .join('');

  root.innerHTML = `
    <section class="screen" aria-label="${s.rhythmLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${s.rhythmLabel}</div>
        <p class="path-intro">${s.rhythmIntro}</p>
        <div class="rhythm-panel">${joints}
          <label class="rhythm-row rhythm-row--sky">
            <input type="checkbox" data-rhythm="bindSky" ${rhythm.bindSky ? 'checked' : ''} />
            <span>${s.rhythmBindSky}</span>
          </label>
        </div>
        <button type="button" class="btn-quiet" data-action="rhythm-save">${s.rhythmSave}</button>
      </div>
    </section>`;
}

function renderSky() {
  const s = t();
  const snap = skySnapshot(new Date(), loadLocation());
  const phaseLabel = s.moonPhases?.[snap.phase] || snap.phase;
  const rituLabel = s.rituNames?.[snap.ritu] || snap.ritu;
  const inner = loadInnerSky();
  const dateKey = localDateKey();
  const marks = inner[dateKey] || [];
  const markChips = Object.entries(s.innerSkyMarks)
    .map(
      ([id, label]) =>
        `<button type="button" class="door-chip ${marks.includes(id) ? 'is-active' : ''}" data-inner-sky="${id}">${label}</button>`,
    )
    .join('');

  root.innerHTML = `
    <section class="screen" aria-label="${s.skyLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${s.skyLabel}</div>
        <p class="path-intro">${s.skyIntro}</p>
        <div class="sky-panel">
          <div class="sky-dome" style="--illum:${snap.illumination.toFixed(3)}" aria-hidden="true">
            <div class="sky-dome__disc"></div>
          </div>
          <dl class="sky-facts">
            <div><dt>${s.skyPhase}</dt><dd>${phaseLabel}</dd></div>
            <div><dt>${s.skyTithi}</dt><dd>${snap.tithi}</dd></div>
            <div><dt>${s.skyRitu}</dt><dd>${rituLabel}</dd></div>
            <div><dt>${s.skySunrise}</dt><dd>${formatMinutes(snap.times.sunrise)}</dd></div>
            <div><dt>${s.skySunset}</dt><dd>${formatMinutes(snap.times.sunset)}</dd></div>
            <div><dt>${s.skyBrahma}</dt><dd>${formatMinutes(snap.times.brahmamuhurta)}</dd></div>
            <div><dt>${s.skyRhythm}</dt><dd>${snap.rhythm}</dd></div>
          </dl>
          <button type="button" class="btn-quiet" data-action="sky-location">${s.skyLocation} · ${snap.locationLabel}</button>
        </div>
        <div class="label label--soft">${s.innerSkyLabel}</div>
        <p class="path-note path-note--muted">${s.innerSkyIntro}</p>
        <div class="door-grid" role="group">${markChips}</div>
      </div>
    </section>`;
}

async function openLivingMap(id) {
  state.livingMap = id;
  state.mapData = await loadLivingMap(id);
  navigate('map-journey');
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

function loadShelf() {
  try {
    return JSON.parse(localStorage.getItem('darshan.contemplationShelf') || '[]');
  } catch {
    return [];
  }
}

function saveToShelf(page) {
  const shelf = loadShelf();
  shelf.unshift({ ...page, saved_at: new Date().toISOString() });
  localStorage.setItem('darshan.contemplationShelf', JSON.stringify(shelf.slice(0, 24)));
}

function renderInquiry() {
  const s = t();
  const doors = s.inquiryDoors
    .map(
      (d) =>
        `<button type="button" class="door-chip ${state.inquiryDoor === d.id ? 'is-active' : ''}" data-door="${d.id}">${d.name}</button>`,
    )
    .join('');

  root.innerHTML = `
    <section class="screen" aria-label="${s.inquiryLabel}">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${s.inquiryLabel}</div>
        <p class="inquiry-intro">${s.inquiryIntro}</p>
        <div class="door-grid" role="group" aria-label="situation">${doors}</div>
        <form class="inquiry-form" data-action="inquiry-submit">
          <label class="sr-only" for="inquiry-field">${s.inquiryPlaceholder}</label>
          <textarea id="inquiry-field" class="inquiry-field" rows="4" maxlength="4000" placeholder="${s.inquiryPlaceholder}">${state.inquiryQuestion || ''}</textarea>
          <button type="submit" class="btn-quiet inquiry-submit">${s.inquirySubmit}</button>
        </form>
      </div>
    </section>`;
}

function renderInquiryResting() {
  const s = t();
  root.innerHTML = `
    <section class="screen inquiry-resting" aria-label="${s.inquiryResting}">
      <div class="breath-glyph" aria-hidden="true"></div>
      <p class="threshold__line">${s.inquiryResting}</p>
    </section>`;
}

function renderContemplation() {
  const s = t();
  const page = state.contemplation;
  if (!page) return navigate('inquiry');

  const citations = (page.envelope.citations || [])
    .map(
      (c) =>
        `<blockquote class="contemplation-quote"><span class="contemplation-quote__bar"></span>${c.quote || c.passage_id}<footer>${c.passage_id}${c.tradition ? ` · ${c.tradition}` : ''}</footer></blockquote>`,
    )
    .join('');

  const movement = page.envelope.offered_movement
    ? `<p class="contemplation-movement"><span class="contemplation-movement__mark">◦</span> ${page.envelope.offered_movement.text} <span class="contemplation-movement__tag">(${s.movementOptional})</span></p>`
    : '';

  const silenceOffer =
    page.envelope.closing === 'honored_silence'
      ? `<button type="button" class="silence-link" data-action="silence">${s.honoredSilenceOffer}</button>`
      : '';

  root.innerHTML = `
    <section class="screen" aria-label="contemplation">
      <div class="container">
        ${renderToolbar()}
        <div class="label">${page.envelope.guidance_mode.replace(/_/g, ' ')}</div>
        <div class="contemplation-body">${page.envelope.body}</div>
        ${citations}
        ${movement}
        ${silenceOffer}
        <div class="contemplation-exits">
          <button type="button" class="btn-quiet" data-action="sit">${s.sitWithIt}</button>
          <button type="button" class="btn-quiet" data-action="keep">${s.keepIt}</button>
          <button type="button" class="btn-quiet" data-action="leave">${s.leaveNow}</button>
        </div>
      </div>
    </section>`;
}

async function submitInquiry(question) {
  const trimmed = question.trim();
  if (trimmed.length < 3) return;

  state.inquiryQuestion = trimmed;
  navigate('inquiry-resting');

  const restingMs = breathDurationMs() > 0 ? 2600 : 400;

  try {
    const res = await fetch('/inquire', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: trimmed, top_k: 5 }),
    });
    if (!res.ok) throw new Error('inquire failed');
    const data = await res.json();
    await new Promise((r) => setTimeout(r, restingMs));
    state.contemplation = data;
    navigate('contemplation');
  } catch {
    await new Promise((r) => setTimeout(r, restingMs));
    state.contemplation = {
      envelope: {
        guidance_mode: 'source_commentary',
        body: 'The well is quiet right now. You may return to the court, or sit in the silence room.',
        citations: [],
        closing: 'plain',
      },
    };
    navigate('contemplation');
  }
}

function navigate(screen) {
  state.screen = screen;
  if (screen !== 'word' && screen !== 'library-read') state.depth = 0;
  if (screen === 'threshold') renderThreshold();
  else if (screen === 'court') renderCourt();
  else if (screen === 'word') renderWord();
  else if (screen === 'library') renderLibraryShelf();
  else if (screen === 'library-read') renderLibraryReading();
  else if (screen === 'inquiry') renderInquiry();
  else if (screen === 'inquiry-resting') renderInquiryResting();
  else if (screen === 'contemplation') renderContemplation();
  else if (screen === 'maps') renderMapsList();
  else if (screen === 'map-journey') renderMapJourney();
  else if (screen === 'practice') renderPractice();
  else if (screen === 'offering') renderOffering();
  else if (screen === 'lookback') renderLookback();
  else if (screen === 'rhythm') renderRhythm();
  else if (screen === 'sky') renderSky();
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
  const el = e.target.closest('[data-action], [data-gesture], [data-shelf], [data-depth], [data-door], [data-map], [data-posture], [data-inner-sky]');
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
    if (el.dataset.action === 'silence' && !['contemplation'].includes(state.screen)) {
      state.silenceReturn = state.screen === 'court' ? 'court' : state.screen;
    }
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
  if (el.dataset.gesture === 'inquiry') navigate('inquiry');
  if (el.dataset.gesture === 'maps') navigate('maps');
  if (el.dataset.gesture === 'practice') navigate('practice');
  if (el.dataset.gesture === 'sky') navigate('sky');
  if (el.dataset.gesture === 'offering') navigate('offering');
  if (el.dataset.gesture === 'lookback') navigate('lookback');
  if (el.dataset.gesture === 'rhythm') navigate('rhythm');
  if (el.dataset.gesture === 'practice-silence') {
    state.silenceReturn = 'practice';
    navigate('silence');
  }
  if (el.dataset.map) openLivingMap(el.dataset.map);
  if (el.dataset.posture) {
    savePosture(el.dataset.posture);
    renderMapJourney();
  }
  if (el.dataset.action === 'map-next' && state.mapData) {
    const step = loadMapStep(state.mapData.id) + 1;
    saveMapStep(state.mapData.id, step);
    renderMapJourney();
  }
  if (el.dataset.action === 'map-stay') navigate('maps');
  if (el.dataset.action === 'rhythm-save') {
    const panel = root.querySelector('.rhythm-panel');
    const rhythm = loadRhythm();
    panel?.querySelectorAll('[data-rhythm]').forEach((input) => {
      rhythm[input.dataset.rhythm] = input.checked;
    });
    saveRhythm(rhythm);
    navigate('practice');
  }
  if (el.dataset.action === 'sky-location') {
    await requestDeviceLocation();
    renderSky();
  }
  if (el.dataset.innerSky) {
    const dateKey = localDateKey();
    const inner = loadInnerSky();
    const marks = new Set(inner[dateKey] || []);
    const id = el.dataset.innerSky;
    if (marks.has(id)) marks.delete(id);
    else marks.add(id);
    inner[dateKey] = [...marks];
    saveInnerSky(inner);
    renderSky();
  }
  if (el.dataset.door) {
    state.inquiryDoor = el.dataset.door;
    renderInquiry();
  }
  if (el.dataset.action === 'sit') {
    state.silenceReturn = 'contemplation';
    navigate('silence');
  }
  if (el.dataset.action === 'keep' && state.contemplation) {
    saveToShelf(state.contemplation);
    closeSession();
  }
  if (el.dataset.action === 'leave') closeSession();
  if (el.dataset.shelf) openLibraryPassage(el.dataset.shelf === 'gita' ? 'gita-ii-47' : el.dataset.shelf);
  if (el.dataset.depth !== undefined) {
    state.depth = Number(el.dataset.depth);
    if (state.screen === 'word') renderWord();
    if (state.screen === 'library-read') renderLibraryReading();
  }
});

root.addEventListener('submit', (e) => {
  const form = e.target.closest('[data-action="inquiry-submit"], [data-action="offering-save"], [data-action="lookback-save"]');
  if (!form) return;
  e.preventDefault();
  if (form.dataset.action === 'inquiry-submit') {
    const field = form.querySelector('#inquiry-field');
    submitInquiry(field?.value || '');
    return;
  }
  if (form.dataset.action === 'offering-save') {
    saveOffering(localDateKey(), form.querySelector('#offering-field')?.value || '');
    navigate('practice');
    return;
  }
  if (form.dataset.action === 'lookback-save') {
    const answers = [...form.querySelectorAll('[data-lookback-idx]')]
      .sort((a, b) => Number(a.dataset.lookbackIdx) - Number(b.dataset.lookbackIdx))
      .map((node) => node.value || '');
    saveLookback(localDateKey(), answers);
    navigate('practice');
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
