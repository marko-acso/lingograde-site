/**
 * Memory Widget — LingoGrade
 * Embeddable sidebar/panel that shows pinned + recent memories for a student.
 *
 * Usage:
 *   <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
 *   <script src="/js/supabase-init.js"></script>
 *   <script src="/js/memory-widget.js"></script>
 *
 *   // Then call:
 *   MemoryWidget.mount('#sidebar', { studentId: 'uuid-here' });
 *
 *   // Or auto-detect from URL param ?student=uuid
 *   MemoryWidget.mount('#sidebar');
 */
var MemoryWidget = (function () {
  'use strict';

  var TABLE = 'client_memories';
  var MAX_PINNED = 5;
  var MAX_RECENT = 5;

  var CATEGORY_LABELS = {
    observation: 'Observation',
    preference: 'Preference',
    trigger: 'Trigger',
    progress: 'Progress',
    logistics: 'Logistics',
    parent_note: 'Parent Note'
  };

  var CATEGORY_COLORS = {
    observation:  { bg: '#EFF6FF', fg: '#2563AB' },
    preference:   { bg: '#FFF7ED', fg: '#C2410C' },
    trigger:      { bg: '#FEF2F2', fg: '#B91C1C' },
    progress:     { bg: '#F0FFF4', fg: '#15803D' },
    logistics:    { bg: '#F5F3FF', fg: '#6D28D9' },
    parent_note:  { bg: '#FFFBEB', fg: '#B45309' }
  };

  function db() { return window.supabase; }

  function esc(str) {
    var d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  // ── Fetch pinned + recent memories ──
  async function fetchMemories(studentId) {
    var pinned = await db()
      .from(TABLE)
      .select('*')
      .eq('student_id', studentId)
      .eq('is_pinned', true)
      .order('updated_at', { ascending: false })
      .limit(MAX_PINNED);

    var pinnedIds = (pinned.data || []).map(function (m) { return m.id; });

    var recentQuery = db()
      .from(TABLE)
      .select('*')
      .eq('student_id', studentId)
      .order('created_at', { ascending: false })
      .limit(MAX_RECENT + pinnedIds.length);

    var recent = await recentQuery;

    // Exclude pinned from recent to avoid duplicates
    var recentFiltered = (recent.data || []).filter(function (m) {
      return pinnedIds.indexOf(m.id) === -1;
    }).slice(0, MAX_RECENT);

    return {
      pinned: pinned.data || [],
      recent: recentFiltered
    };
  }

  // ── Render a single memory card ──
  function renderCard(m) {
    var cat = CATEGORY_COLORS[m.category] || { bg: '#F3F4F6', fg: '#6B7280' };
    var dateStr = m.session_date || m.created_at.substring(0, 10);
    var tags = (m.tags || []).map(function (t) {
      return '<span style="font-size:0.6875rem;padding:1px 6px;background:#F3F4F6;border-radius:6px;color:#8A8A8A;">' + esc(t) + '</span>';
    }).join(' ');

    return '<div style="background:white;border-radius:10px;border:1px solid #E0E0E0;padding:14px 16px;' +
      (m.is_pinned ? 'border-left:3px solid #2563AB;' : '') + '">' +
      '<div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;">' +
        '<span style="font-size:0.625rem;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;padding:2px 8px;border-radius:10px;background:' + cat.bg + ';color:' + cat.fg + ';">' + CATEGORY_LABELS[m.category] + '</span>' +
        '<span style="font-size:0.6875rem;color:#8A8A8A;">' + dateStr + '</span>' +
        (m.is_pinned ? '<span style="font-size:0.6875rem;color:#2563AB;" title="Pinned">&#9733;</span>' : '') +
      '</div>' +
      '<div style="font-family:\'DM Serif Display\',Georgia,serif;font-size:0.9375rem;margin-bottom:3px;">' + esc(m.title) + '</div>' +
      '<div style="font-size:0.8125rem;color:#4A4A4A;line-height:1.55;white-space:pre-wrap;max-height:4.8em;overflow:hidden;">' + esc(m.body) + '</div>' +
      (tags ? '<div style="display:flex;gap:4px;margin-top:8px;flex-wrap:wrap;">' + tags + '</div>' : '') +
    '</div>';
  }

  // ── Render section ──
  function renderSection(title, memories) {
    if (!memories.length) return '';
    var cards = memories.map(renderCard).join('');
    return '<div style="margin-bottom:16px;">' +
      '<div style="font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;color:#8A8A8A;margin-bottom:8px;">' + title + '</div>' +
      '<div style="display:flex;flex-direction:column;gap:8px;">' + cards + '</div>' +
    '</div>';
  }

  // ── Mount widget into a container ──
  async function mount(selector, opts) {
    opts = opts || {};
    var container = typeof selector === 'string' ? document.querySelector(selector) : selector;
    if (!container) { console.error('[MemoryWidget] Container not found:', selector); return; }

    var studentId = opts.studentId || new URLSearchParams(window.location.search).get('student');
    if (!studentId) {
      container.innerHTML = '<div style="padding:16px;color:#8A8A8A;font-size:0.8125rem;">No student selected.</div>';
      return;
    }

    container.innerHTML = '<div style="padding:16px;color:#8A8A8A;font-size:0.8125rem;">Loading memories...</div>';

    var session = await db().auth.getSession();
    if (!session.data.session) {
      container.innerHTML = '<div style="padding:16px;color:#C0392B;font-size:0.8125rem;">Sign in to view client memories.</div>';
      return;
    }

    var data = await fetchMemories(studentId);

    if (!data.pinned.length && !data.recent.length) {
      container.innerHTML = '<div style="padding:20px;text-align:center;">' +
        '<div style="font-family:\'DM Serif Display\',Georgia,serif;font-size:1rem;color:#4A4A4A;margin-bottom:4px;">No memories yet</div>' +
        '<div style="font-size:0.8125rem;color:#8A8A8A;">Notes added in <a href="/client-memory.html?student=' + studentId + '" style="color:#2563AB;text-decoration:none;">Client Memory</a> will appear here.</div>' +
      '</div>';
      return;
    }

    var html = '<div style="font-family:\'DM Sans\',-apple-system,sans-serif;">' +
      '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">' +
        '<div style="font-family:\'DM Serif Display\',Georgia,serif;font-size:1.05rem;">Client Memory</div>' +
        '<a href="/client-memory.html?student=' + studentId + '" style="font-size:0.75rem;color:#2563AB;text-decoration:none;">View all</a>' +
      '</div>' +
      renderSection('Pinned', data.pinned) +
      renderSection('Recent', data.recent) +
    '</div>';

    container.innerHTML = html;
  }

  return { mount: mount };
})();
