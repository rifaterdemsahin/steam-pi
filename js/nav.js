/**
 * Steam-Pi — Shared Navigation
 * Reads nav.json, builds debug bar + main nav + search + mobile menu.
 * Debug mode persists in cookie: debug=true
 */
(function () {
  'use strict';

  const BASE = window.BASE_PATH || './';

  /* ── Cookie helpers ──────────────────────────────────────── */
  function getCookie(name) {
    return document.cookie.split('; ').reduce((acc, pair) => {
      const [k, v] = pair.split('=');
      return k === name ? decodeURIComponent(v) : acc;
    }, null);
  }

  function setCookie(name, value, days) {
    const exp = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)};expires=${exp};path=/`;
  }

  /* ── Resolve href relative to root ──────────────────────── */
  function href(path) {
    return BASE + path;
  }

  /* ── Build nav HTML ──────────────────────────────────────── */
  function buildNav(data) {
    const isDebug = getCookie('debug') === 'true';

    const debugLinks = data.debugMenu.map(item =>
      `<a href="${href(item.href)}">${item.emoji} ${item.label}</a>`
    ).join('');

    const contentLinks = data.contentMenu.map(item =>
      `<a href="${href(item.href)}" class="nav-link">${item.emoji} ${item.label}</a>`
    ).join('');

    const mobileLinks = data.contentMenu.map(item =>
      `<a href="${href(item.href)}" class="mobile-link">${item.emoji} ${item.label}</a>`
    ).join('');

    const html = `
      <div class="debug-bar${isDebug ? '' : ' hidden'}" id="debug-bar">
        ${debugLinks}
      </div>
      <nav class="main-nav" role="navigation" aria-label="Main navigation">
        <div class="nav-bar">
          <a href="${href('index.html')}" class="nav-brand">🎮 Steam-Pi</a>

          <div class="nav-search-wrap" role="search">
            <input
              type="text"
              id="nav-search"
              placeholder="🔍 Search pages…"
              autocomplete="off"
              aria-label="Search"
            />
            <div id="search-results" class="search-dropdown hidden" role="listbox"></div>
          </div>

          <div class="nav-links" id="nav-links" role="menubar">
            ${contentLinks}
          </div>

          <button
            id="debug-btn"
            class="debug-btn${isDebug ? ' active' : ''}"
            title="Toggle debug framework menu"
            aria-pressed="${isDebug}"
          >🐛 Debug</button>

          <button id="hamburger" class="hamburger" aria-label="Toggle mobile menu" aria-expanded="false">☰</button>
        </div>

        <div class="mobile-menu hidden" id="mobile-menu" role="menu">
          ${mobileLinks}
        </div>
      </nav>
    `;

    const container = document.getElementById('nav-container');
    if (container) {
      container.innerHTML = html;
    } else {
      // Prepend to body if no container
      const wrapper = document.createElement('div');
      wrapper.innerHTML = html;
      document.body.prepend(wrapper);
    }

    wireEvents(data.searchIndex || []);
    highlightActive();
  }

  /* ── Wire events ─────────────────────────────────────────── */
  function wireEvents(searchIndex) {
    // Debug toggle
    const debugBtn = document.getElementById('debug-btn');
    const debugBar = document.getElementById('debug-bar');

    if (debugBtn && debugBar) {
      debugBtn.addEventListener('click', () => {
        const active = debugBar.classList.toggle('hidden');
        const isNowDebug = !active; // hidden toggled, so if hidden was added = not debug
        const nowActive = !debugBar.classList.contains('hidden');
        setCookie('debug', nowActive ? 'true' : 'false', 365);
        debugBtn.classList.toggle('active', nowActive);
        debugBtn.setAttribute('aria-pressed', nowActive);
      });
    }

    // Hamburger
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');

    if (hamburger && mobileMenu) {
      hamburger.addEventListener('click', () => {
        const open = mobileMenu.classList.toggle('hidden');
        hamburger.setAttribute('aria-expanded', !mobileMenu.classList.contains('hidden'));
      });
    }

    // Search
    setupSearch(searchIndex);
  }

  /* ── Search autocomplete ─────────────────────────────────── */
  function setupSearch(index) {
    const input = document.getElementById('nav-search');
    const dropdown = document.getElementById('search-results');
    if (!input || !dropdown) return;

    let activeIdx = -1;
    let results = [];

    function render(items) {
      results = items;
      activeIdx = -1;
      if (items.length === 0) {
        dropdown.classList.add('hidden');
        return;
      }
      dropdown.innerHTML = items.slice(0, 8).map((item, i) =>
        `<a href="${href(item.url)}" class="search-item" role="option" data-idx="${i}">
          <span class="search-item-title">${item.title}</span>
          ${item.tags ? `<span class="search-item-tag">${item.tags[0]}</span>` : ''}
        </a>`
      ).join('');
      dropdown.classList.remove('hidden');
    }

    function close() {
      dropdown.classList.add('hidden');
      activeIdx = -1;
    }

    function setActive(idx) {
      const items = dropdown.querySelectorAll('.search-item');
      items.forEach((el, i) => el.classList.toggle('active', i === idx));
      activeIdx = idx;
    }

    let debounceTimer;
    input.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        const q = input.value.trim().toLowerCase();
        if (!q) { close(); return; }
        const matches = index.filter(item =>
          item.title.toLowerCase().includes(q) ||
          (item.tags || []).some(t => t.includes(q))
        );
        render(matches);
      }, 120);
    });

    input.addEventListener('keydown', e => {
      if (dropdown.classList.contains('hidden')) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(Math.min(activeIdx + 1, results.length - 1)); }
      if (e.key === 'ArrowUp')   { e.preventDefault(); setActive(Math.max(activeIdx - 1, 0)); }
      if (e.key === 'Enter' && activeIdx >= 0) {
        const items = dropdown.querySelectorAll('.search-item');
        if (items[activeIdx]) items[activeIdx].click();
      }
      if (e.key === 'Escape') { close(); input.blur(); }
    });

    document.addEventListener('click', e => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) close();
    });
  }

  /* ── Highlight current page in nav ──────────────────────── */
  function highlightActive() {
    const path = window.location.pathname + window.location.search;
    document.querySelectorAll('.nav-link').forEach(link => {
      const linkPath = new URL(link.href, window.location.href).pathname;
      link.classList.toggle('active', linkPath === window.location.pathname);
    });
  }

  /* ── Fetch nav.json and boot ─────────────────────────────── */
  fetch(BASE + 'nav.json')
    .then(r => { if (!r.ok) throw new Error('nav.json not found'); return r.json(); })
    .then(buildNav)
    .catch(err => {
      console.warn('[nav.js] Could not load nav.json:', err.message);
      // Fallback minimal nav
      const container = document.getElementById('nav-container');
      if (container) {
        container.innerHTML = `<nav class="main-nav"><div class="nav-bar">
          <a href="${href('index.html')}" class="nav-brand">🎮 Steam-Pi</a>
        </div></nav>`;
      }
    });
})();
