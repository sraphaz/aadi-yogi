/** Living corpus bundle version + growth notice (RF-038). */

const VERSION_KEY = 'darshan.corpusVersion';
const DISMISS_KEY = 'darshan.corpusGrowthDismissed';

export function loadSeenCorpusVersion() {
  return localStorage.getItem(VERSION_KEY) || '';
}

export function saveSeenCorpusVersion(version) {
  if (version) localStorage.setItem(VERSION_KEY, version);
}

export function isGrowthNoticeDismissed(version) {
  return localStorage.getItem(DISMISS_KEY) === version;
}

export function dismissGrowthNotice(version) {
  if (version) localStorage.setItem(DISMISS_KEY, version);
}

export function shouldShowGrowthNotice(catalog) {
  if (!catalog?.bundle_version) return false;
  const seen = loadSeenCorpusVersion();
  if (!seen) {
    saveSeenCorpusVersion(catalog.bundle_version);
    return false;
  }
  if (catalog.bundle_version === seen) return false;
  if (isGrowthNoticeDismissed(catalog.bundle_version)) return false;
  return true;
}

export function acknowledgeCorpusVersion(catalog) {
  if (catalog?.bundle_version) saveSeenCorpusVersion(catalog.bundle_version);
}
