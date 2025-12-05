/* ====== scripts.js (generated) ====== */

/* Helper: escape regex special chars */
function escapeRegex(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/* Save original innerHTML of each td once (so we can restore) */
(function cacheCellOriginalsOnce() {
    document.addEventListener('DOMContentLoaded', function() {
        const tds = document.querySelectorAll('#dataTable tbody td');
        tds.forEach(td => {
            if (!td.dataset.original) td.dataset.original = td.innerHTML;
        });
    });
})();

/* Highlight matches in text nodes under an element, preserving tags (links etc) */
function highlightUnderElement(el, term) {
    if (!term) return;
    const regex = new RegExp(escapeRegex(term), 'gi');

    function walk(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            const text = node.nodeValue;
            const match = regex.exec(text);
            if (match) {
                regex.lastIndex = 0; // reset for subsequent calls
                const frag = document.createDocumentFragment();
                let lastIndex = 0;
                let m;
                while ((m = regex.exec(text)) !== null) {
                    const before = text.slice(lastIndex, m.index);
                    if (before) frag.appendChild(document.createTextNode(before));
                    const mark = document.createElement('mark');
                    mark.textContent = m[0];
                    frag.appendChild(mark);
                    lastIndex = m.index + m[0].length;
                }
                const after = text.slice(lastIndex);
                if (after) frag.appendChild(document.createTextNode(after));
                node.parentNode.replaceChild(frag, node);
            }
        } else if (node.nodeType === Node.ELEMENT_NODE && node.tagName.toLowerCase() !== 'script' && node.tagName.toLowerCase() !== 'style') {
            const children = Array.from(node.childNodes);
            for (const child of children) walk(child);
        }
    }

    walk(el);
}

/* Global active status filter (null = no status filter) */
let activeStatusFilter = null;

/* Helper: normalize status text for comparison */
function normStatusText(s) {
  if (!s) return '';
  return s.toString().trim().toLowerCase();
}

/* Toggle status filter: same button toggles on/off */
function toggleStatusFilter(statusKey) {
  if (activeStatusFilter === statusKey) activeStatusFilter = null;
  else activeStatusFilter = statusKey;

  // visually update FABs if they exist
  const notBtn = document.getElementById('filterNotCalledBtn');
  const whatsBtn = document.getElementById('filterWhatsAppBtn');
  if (notBtn) notBtn.classList.toggle('active', activeStatusFilter === 'not called');
  if (whatsBtn) whatsBtn.classList.toggle('active', activeStatusFilter === 'whatsapp');

  searchTable();
}

/* Clear highlights + clear active filters + clear search input */
function clearHighlightsAndSearch() {
  activeStatusFilter = null;
  const notBtn = document.getElementById('filterNotCalledBtn');
  const whatsBtn = document.getElementById('filterWhatsAppBtn');
  if (notBtn) notBtn.classList.remove('active');
  if (whatsBtn) whatsBtn.classList.remove('active');

  const input = document.getElementById('searchInput');
  if (input) input.value = '';

  const tds = document.querySelectorAll('#dataTable tbody td');
  tds.forEach(td => {
    if (td.dataset && td.dataset.original !== undefined) {
      td.innerHTML = td.dataset.original;
    }
  });

  const rows = document.querySelectorAll('#dataTable tbody tr');
  rows.forEach(r => r.style.display = '');
  const nr = document.getElementById('noResults');
  if (nr) nr.style.display = 'none';
}

/* Simple go-to-top */
function goToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* searchTable() that respects activeStatusFilter and highlights */
function searchTable() {
  const input = document.getElementById('searchInput');
  const filter = (input && input.value || '').trim().toLowerCase();
  const rows = document.querySelectorAll('#dataTable tbody tr');
  let foundAny = false;

  rows.forEach(row => {
    const tds = row.querySelectorAll('td');
    // restore original
    tds.forEach(td => {
      if (td.dataset && td.dataset.original !== undefined) {
        td.innerHTML = td.dataset.original;
      }
    });

    const rowText = (row.textContent || '').toLowerCase();
    const textMatch = !filter || rowText.includes(filter);

    // status match
    let statusMatch = true;
    if (activeStatusFilter) {
      statusMatch = false;
      const statusCandidates = Array.from(row.querySelectorAll('td')).map(td => (td.textContent || '').toLowerCase());
      for (const cellText of statusCandidates) {
        if (activeStatusFilter === 'not called') {
          if (cellText.includes('not called')) { statusMatch = true; break; }
        } else if (activeStatusFilter === 'whatsapp') {
          if (cellText.includes('whatsapp')) { statusMatch = true; break; }
        } else {
          if (cellText.includes(activeStatusFilter)) { statusMatch = true; break; }
        }
      }
    }

    const isMatch = textMatch && statusMatch;
    row.style.display = isMatch ? '' : 'none';

    if (isMatch && filter) {
      tds.forEach(td => {
        if ((td.textContent || '').toLowerCase().includes(filter)) {
          highlightUnderElement(td, filter);
        }
      });
    }

    if (isMatch) foundAny = true;
  });

  const nr = document.getElementById('noResults');
  if (nr) nr.style.display = (foundAny || !filter ? 'none' : 'block');

  // update counts after filtering
  if (typeof updateStatusCounts === 'function') {
    setTimeout(updateStatusCounts, 40);
  }
}

/* Helper: read normalized status text from a row */
function getStatusFromRow(row) {
  const badge = row.querySelector('span.badge');
  if (badge && badge.textContent) return normStatusText(badge.textContent);
  const text = normStatusText(row.textContent || '');
  const keys = ['not called','whatsapp','confirmed','maybe','phone busy','busy','not reachable','not coming'];
  for (const k of keys) if (text.includes(k)) return k;
  return '';
}

/* Update counts for toolbar */
function updateStatusCounts() {
  const rows = Array.from(document.querySelectorAll('#dataTable tbody tr'));
  const counts = {'not called':0,'whatsapp':0,'confirmed':0,'maybe':0,'busy':0,'not reachable':0,'not coming':0};
  let visible = 0;
  rows.forEach(row => {
    const s = getStatusFromRow(row);
    if (s.includes('confirmed')) counts['confirmed']++;
    else if (s.includes('maybe')) counts['maybe']++;
    else if (s.includes('whatsapp')) counts['whatsapp']++;
    else if (s.includes('not called')) counts['not called']++;
    else if (s.includes('busy') || s.includes('phone busy')) counts['busy']++;
    else if (s.includes('not reachable')) counts['not reachable']++;
    else if (s.includes('not coming')) counts['not coming']++;

    const cs = window.getComputedStyle(row);
    if (cs.display !== 'none' && cs.visibility !== 'hidden' && row.offsetParent !== null) visible++;
  });

  // write counts to DOM safely
  const safeSet = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
  safeSet('count-notcalled', counts['not called']);
  safeSet('count-whatsapp', counts['whatsapp']);
  safeSet('count-confirmed', counts['confirmed']);
  safeSet('count-maybe', counts['maybe']);
  safeSet('count-busy', counts['busy']);
  safeSet('count-nr', counts['not reachable']);
  safeSet('count-no', counts['not coming']);

  safeSet('totalVisible', visible);
  safeSet('totalAll', rows.length);
}

/* toolbar integration helper */
function toggleStatusFilterFromToolbar(statusKey) {
  if (activeStatusFilter === statusKey) activeStatusFilter = null;
  else activeStatusFilter = statusKey;

  document.querySelectorAll('.status-filter-btn').forEach(btn => {
    const k = btn.getAttribute('data-status-key');
    btn.classList.toggle('active', activeStatusFilter === k);
  });

  if (typeof searchTable === 'function') searchTable();
  else applyStatusFilterDirectly();
  setTimeout(updateStatusCounts, 50);
  toggleStatusDropdown(false);
}

function applyStatusFilterDirectly() {
  const rows = document.querySelectorAll('#dataTable tbody tr');
  rows.forEach(row => {
    if (!activeStatusFilter) { row.style.display = ''; return; }
    const s = getStatusFromRow(row);
    if ((s || '').includes(activeStatusFilter)) row.style.display = '';
    else row.style.display = 'none';
  });
  updateStatusCounts();
}

/* ensure counts on load + wire search input to counts */
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('#dataTable tbody td').forEach(td => {
    if (td.dataset.original === undefined) td.dataset.original = td.innerHTML;
  });

  updateStatusCounts();

  const input = document.getElementById('searchInput');
  if (input) {
    let to; input.addEventListener('input', function() {
      clearTimeout(to);
      to = setTimeout(function() {
        if (typeof searchTable === 'function') searchTable();
        updateStatusCounts();
      }, 150);
    });
  }

  const tbody = document.querySelector('#dataTable tbody');
  if (tbody) {
    tbody.addEventListener('click', function() { setTimeout(updateStatusCounts, 40); });
  }

  // MutationObserver to auto-update counts when rows change
  (function() {
    const table = document.querySelector('#dataTable');
    if (!table) return;
    const observer = new MutationObserver(function() { setTimeout(updateStatusCounts, 50); });
    const tb = table.querySelector('tbody') || table;
    observer.observe(tb, { childList: true, subtree: true, characterData: true });
  })();
});

// Dropdown toggle for compact toolbar
function toggleStatusDropdown(force) {
  const panel = document.getElementById('statusDropdownPanel');
  const toggle = document.getElementById('statusDropdownToggle');
  if (!panel || !toggle) return;
  const isOpen = panel.classList.contains('open');
  const willOpen = (typeof force === 'boolean') ? force : !isOpen;

  panel.classList.toggle('open', willOpen);
  panel.setAttribute('aria-hidden', willOpen ? 'false' : 'true');
  toggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');

  // if opening, focus first button for accessibility
  if (willOpen) {
    const first = panel.querySelector('.status-filter-btn');
    if (first) first.focus();
    // add listeners to close when clicking outside or pressing ESC
    document.addEventListener('click', outsideClickHandler);
    document.addEventListener('keydown', escHandler);
  } else {
    document.removeEventListener('click', outsideClickHandler);
    document.removeEventListener('keydown', escHandler);
  }
}

function outsideClickHandler(e) {
  const wrap = document.getElementById('statusDropdownWrap');
  const panel = document.getElementById('statusDropdownPanel');
  const toggle = document.getElementById('statusDropdownToggle');
  if (!panel || !toggle) return;
  if (wrap && !wrap.contains(e.target)) {
    toggleStatusDropdown(false);
  }
}

function escHandler(e) {
  if (e.key === 'Escape' || e.key === 'Esc') {
    toggleStatusDropdown(false);
  }
}

// Keep mini total in toggle updated whenever counts change
(function mirrorTotalsToMini() {
  const updateMini = function() {
    const tv = document.getElementById('totalVisible');
    const ta = document.getElementById('totalAll');
    const mini = document.getElementById('miniTotal');
    if (!mini) return;
    const v = tv ? tv.textContent : '';
    const t = ta ? ta.textContent : '';
    mini.textContent = (v !== null && t !== null) ? `${v} / ${t}` : '';
  };

  // wrap updateStatusCounts if present so it also updates mini total
  if (typeof updateStatusCounts === 'function') {
    const orig = updateStatusCounts;
    window.updateStatusCounts = function() {
      orig();
      updateMini();
    };
  } else {
    // otherwise call periodically once DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(updateMini, 80);
    });
  }

  // Also update mini when totals change via clicks (defensive)
  document.addEventListener('click', () => setTimeout(updateMini, 60));
})();
