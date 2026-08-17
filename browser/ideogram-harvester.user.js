// ==UserScript==
// @name         Content Universe - Ideogram Harvester
// @namespace    https://github.com/AvaTar-ArTs/content-universe
// @version      0.3.0
// @description  Passive Ideogram identity harvester with adaptive lazy-load scrolling, resume, and export.
// @match        https://ideogram.ai/*
// @grant        GM_setClipboard
// ==/UserScript==

(() => {
  'use strict';

  const STORAGE_KEY = 'content-universe:ideogram:observations:v1';
  const CONFIG = {
    scanDelayMs: 200,
    scrollStep: 750,
    scrollIntervalMs: 1200,
    maxIdleCycles: 20,
    reverseNudge: 80,
    persistEvery: 25,
  };

  const records = new Map();
  const RESPONSE_RE = /\/response\/([^/@?]+)(?:@([^/?]+))?/;
  const GENERATION_RE = /^\/g\/([^/]+)\/(\d+)/;
  let scrollTimer = null;
  let targetScroller = null;
  let mutationTimer = null;
  let mutationsSincePersist = 0;

  function restore() {
    try {
      const saved = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '[]');
      if (Array.isArray(saved)) {
        saved.forEach(item => {
          const key = item.response_id || `${item.generation_id}:${item.response_index ?? 'unknown'}`;
          records.set(key, item);
        });
      }
    } catch (error) {
      console.warn('[Content Universe] resume data unreadable', error);
    }
  }

  function persist() {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify([...records.values()]));
      mutationsSincePersist = 0;
    } catch (error) {
      console.warn('[Content Universe] resume persistence failed', error);
    }
  }

  function observationFromCard(card) {
    const generationId = card.getAttribute('data-testid')?.replace('image-grid-item-', '');
    if (!generationId) return null;

    const link = card.querySelector('a[href^="/g/"]');
    const image = card.querySelector('img[src*="/response/"]');
    const gm = link?.getAttribute('href')?.match(GENERATION_RE);
    const am = image?.src?.match(RESPONSE_RE);
    const responseId = am?.[1] || null;
    const responseIndex = gm ? Number(gm[2]) : null;

    return {
      platform: 'ideogram',
      generation_id: generationId,
      response_id: responseId,
      response_index: responseIndex,
      generation_url: link?.href || null,
      asset_url: image?.src || null,
      asset_resolution: am?.[2] || null,
      feed: card.closest('[data-feed]')?.getAttribute('data-feed') || null,
      observed_at: new Date().toISOString(),
      source: 'ideogram-userscript-dom',
    };
  }

  function scan() {
    let added = 0;
    document.querySelectorAll('[data-testid^="image-grid-item-"]').forEach(card => {
      const item = observationFromCard(card);
      if (!item) return;
      const key = item.response_id || `${item.generation_id}:${item.response_index ?? 'unknown'}`;
      const existing = records.get(key);
      if (!existing) added += 1;
      records.set(key, {...existing, ...item});
    });

    mutationsSincePersist += added;
    if (added && mutationsSincePersist >= CONFIG.persistEvery) persist();
    updatePanel();
    return added;
  }

  function debouncedScan() {
    clearTimeout(mutationTimer);
    mutationTimer = setTimeout(scan, CONFIG.scanDelayMs);
  }

  function candidateScrollers() {
    const nodes = [document.scrollingElement, ...document.querySelectorAll('[data-feed], main, [role="main"], div')];
    return nodes.filter(Boolean).filter(el => {
      if (el === document.scrollingElement) return true;
      const style = getComputedStyle(el);
      const scrollable = /(auto|scroll)/.test(style.overflowY);
      return scrollable && el.scrollHeight > el.clientHeight + 300;
    });
  }

  function findBestScroller() {
    const candidates = candidateScrollers();
    candidates.sort((a, b) => (b.scrollHeight - b.clientHeight) - (a.scrollHeight - a.clientHeight));
    return candidates[0] || document.scrollingElement || window;
  }

  function scrollByAmount(target, amount) {
    if (target === window || target === document.scrollingElement || target === document.documentElement || target === document.body) {
      window.scrollBy({top: amount, behavior: 'smooth'});
    } else if (typeof target.scrollBy === 'function') {
      target.scrollBy({top: amount, behavior: 'smooth'});
    }
  }

  function startScroll() {
    if (scrollTimer) return;
    targetScroller = findBestScroller();
    let lastCount = records.size;
    let idleCycles = 0;
    setStatus('Auto-scroll running', 'active');

    scrollTimer = setInterval(() => {
      scan();
      scrollByAmount(targetScroller, CONFIG.scrollStep);
      const current = records.size;
      if (current === lastCount) {
        idleCycles += 1;
        setStatus(`Waiting for lazy load ${idleCycles}/${CONFIG.maxIdleCycles}`, 'waiting');
        if (idleCycles % 5 === 0) scrollByAmount(targetScroller, -CONFIG.reverseNudge);
        if (idleCycles >= CONFIG.maxIdleCycles) stopScroll('No new identities; likely end of feed');
      } else {
        lastCount = current;
        idleCycles = 0;
        setStatus(`Harvesting · ${current} identities`, 'active');
      }
    }, CONFIG.scrollIntervalMs);
    updatePanel();
  }

  function stopScroll(reason = 'Paused') {
    if (scrollTimer) clearInterval(scrollTimer);
    scrollTimer = null;
    persist();
    setStatus(reason, 'idle');
    updatePanel();
  }

  function clearSession() {
    if (!confirm('Clear Content Universe observations from this browser session?')) return;
    stopScroll('Cleared');
    records.clear();
    sessionStorage.removeItem(STORAGE_KEY);
    updatePanel();
  }

  function serialized() {
    return JSON.stringify([...records.values()], null, 2);
  }

  function copyJson() {
    const text = serialized();
    if (typeof GM_setClipboard === 'function') GM_setClipboard(text);
    else navigator.clipboard.writeText(text);
    setStatus('JSON copied', 'active');
  }

  function exportJson() {
    persist();
    const blob = new Blob([serialized()], {type: 'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `content-universe-ideogram-${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    setStatus('JSON exported', 'active');
  }

  function setStatus(text, state = 'idle') {
    const el = document.getElementById('cu-status');
    if (!el) return;
    el.textContent = text;
    el.style.color = state === 'active' ? '#86efac' : state === 'waiting' ? '#fde68a' : '#a1a1aa';
  }

  function createPanel() {
    if (document.getElementById('cu-ideogram-panel')) return;
    const panel = document.createElement('div');
    panel.id = 'cu-ideogram-panel';
    panel.style.cssText = [
      'position:fixed','right:16px','bottom:16px','z-index:2147483647','background:#111','color:#fff',
      'border:1px solid #3f3f46','border-radius:14px','padding:12px','font:12px system-ui',
      'box-shadow:0 8px 30px #0009','min-width:248px','backdrop-filter:blur(10px)'
    ].join(';');
    panel.innerHTML = `
      <div style="display:flex;justify-content:space-between;gap:10px;align-items:center">
        <strong style="font-size:13px">◈ Content Universe</strong>
        <span id="cu-count" style="color:#c4b5fd">0</span>
      </div>
      <div id="cu-status" style="color:#a1a1aa;margin:6px 0 10px">Ready</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">
        <button id="cu-scan">Scan</button>
        <button id="cu-scroll">Auto-scroll</button>
        <button id="cu-copy">Copy JSON</button>
        <button id="cu-export">Export</button>
      </div>
      <button id="cu-clear" style="width:100%;margin-top:6px;opacity:.7">Clear session</button>`;
    panel.querySelectorAll('button').forEach(button => {
      button.style.cssText = 'background:#27272a;color:#fff;border:1px solid #52525b;border-radius:8px;padding:7px;cursor:pointer';
    });
    document.body.appendChild(panel);
    panel.querySelector('#cu-scan').onclick = () => { const n = scan(); setStatus(`Scan complete · +${n}`, 'active'); };
    panel.querySelector('#cu-scroll').onclick = () => scrollTimer ? stopScroll() : startScroll();
    panel.querySelector('#cu-copy').onclick = copyJson;
    panel.querySelector('#cu-export').onclick = exportJson;
    panel.querySelector('#cu-clear').onclick = clearSession;
  }

  function updatePanel() {
    const count = document.getElementById('cu-count');
    if (count) count.textContent = `${records.size} IDs`;
    const scroll = document.getElementById('cu-scroll');
    if (scroll) scroll.textContent = scrollTimer ? 'Stop scroll' : 'Auto-scroll';
  }

  restore();
  const observer = new MutationObserver(debouncedScan);
  window.addEventListener('load', () => {
    createPanel();
    scan();
    observer.observe(document.body, {subtree: true, childList: true});
    setStatus(records.size ? `Resumed ${records.size} identities` : 'Ready', records.size ? 'active' : 'idle');
  });

  window.addEventListener('beforeunload', persist);
  window.ContentUniverseIdeogram = {records, scan, startScroll, stopScroll, exportJson, persist};
})();
