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
  // Replace these with your actual Supabase project values
  var SUPABASE_URL  = 'https://YOUR_PROJECT.supabase.co';
  var SUPABASE_ANON = 'YOUR_ANON_KEY';

  if (typeof window.supabase !== 'undefined') return; // already initialized

  if (typeof window.supabaseJs === 'undefined' && typeof window.supabase === 'undefined') {
    console.error('[LingoGrade] Supabase JS library not loaded. Add the CDN script before supabase-init.js');
    return;
  }

  var createClient = (window.supabaseJs || window.supabase).createClient;
  window.supabase = createClient(SUPABASE_URL, SUPABASE_ANON);
})();
