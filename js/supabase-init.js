/**
 * Supabase Client Init — LingoGrade
 *
 * Usage: include after the Supabase CDN script:
 *   <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
 *   <script src="/js/supabase-init.js"></script>
 *
 * Then use window.supabase anywhere.
 */
(function () {
  'use strict';

  // ── Config ──
  var SUPABASE_URL  = 'https://sbfjhsfvsbyjguplywfj.supabase.co';
  var SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNiZmpoc2Z2c2J5amd1cGx5d2ZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM1Nzg3ODgsImV4cCI6MjA4OTE1NDc4OH0.i9Wua_EZWY-Vvr8860rAIaN3uN74M4MHDsKEgyQMKfQ';

  if (typeof window.supabase !== 'undefined') return; // already initialized

  if (typeof window.supabaseJs === 'undefined' && typeof window.supabase === 'undefined') {
    console.error('[LingoGrade] Supabase JS library not loaded. Add the CDN script before supabase-init.js');
    return;
  }

  var createClient = (window.supabaseJs || window.supabase).createClient;
  window.supabase = createClient(SUPABASE_URL, SUPABASE_ANON);
})();
