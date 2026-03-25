/**
 * LingoGrade Shield v1.0 — Invisible Bot Detection
 *
 * Analyzes mouse movement, scroll behavior, keystroke rhythm, and touch
 * patterns to compute a "human score" (0-100). No CAPTCHA, no UI.
 *
 * Score thresholds:
 *   > 60  — human, allow submission
 *   30-60 — suspicious, allow but flag
 *   < 30  — likely bot, block silently
 *
 * Self-initializing: include <script src="js/shield.js" defer></script>
 */
;(function () {
  'use strict';

  // ── Config ──
  var FIELD_NAME  = '_shield';
  var BLOCK_SCORE = 30;
  var FLAG_SCORE  = 60;
  var VERSION     = '1.0';
  var MAX_POINTS  = 500;   // cap stored trajectory points

  // ── State ──
  var mouse   = [];  // {x, y, t}
  var scrolls = [];  // {y, t}
  var keys    = [];  // {t}  (timestamps only — no keylogging)
  var touches = [];  // {x, y, t, dur}
  var startTs = Date.now();

  // ── Collectors ──

  function onMouse(e) {
    if (mouse.length >= MAX_POINTS) return;
    mouse.push({ x: e.clientX, y: e.clientY, t: Date.now() });
  }

  function onScroll() {
    scrolls.push({ y: window.scrollY || window.pageYOffset, t: Date.now() });
  }

  function onKey() {
    keys.push({ t: Date.now() });
  }

  var touchStart = null;
  function onTouchStart(e) {
    var touch = e.touches[0];
    if (touch) touchStart = { x: touch.clientX, y: touch.clientY, t: Date.now() };
  }
  function onTouchEnd(e) {
    if (!touchStart) return;
    var touch = e.changedTouches[0];
    if (touch) {
      touches.push({
        x: touch.clientX - touchStart.x,
        y: touch.clientY - touchStart.y,
        t: touchStart.t,
        dur: Date.now() - touchStart.t
      });
    }
    touchStart = null;
  }

  // ── Math helpers ──

  function variance(arr) {
    if (arr.length < 2) return 0;
    var mean = 0;
    for (var i = 0; i < arr.length; i++) mean += arr[i];
    mean /= arr.length;
    var sum = 0;
    for (var j = 0; j < arr.length; j++) sum += (arr[j] - mean) * (arr[j] - mean);
    return sum / (arr.length - 1);
  }

  function clamp(v, lo, hi) {
    return v < lo ? lo : v > hi ? hi : v;
  }

  // ── Metric computations ──

  /** Path curvature: ratio of actual distance to straight-line distance. Humans > 1.05 */
  function curveScore() {
    if (mouse.length < 10) return 0;
    var totalDist = 0, i;
    for (i = 1; i < mouse.length; i++) {
      var dx = mouse[i].x - mouse[i - 1].x;
      var dy = mouse[i].y - mouse[i - 1].y;
      totalDist += Math.sqrt(dx * dx + dy * dy);
    }
    var sx = mouse[mouse.length - 1].x - mouse[0].x;
    var sy = mouse[mouse.length - 1].y - mouse[0].y;
    var straight = Math.sqrt(sx * sx + sy * sy);
    if (straight < 5) return 15; // mouse stayed mostly still — probably human idle
    var ratio = totalDist / straight;
    // Humans typically 1.1-3.0, bots ~1.0
    if (ratio > 1.5) return 25;
    if (ratio > 1.15) return 20;
    if (ratio > 1.05) return 12;
    return 2; // suspiciously straight
  }

  /** Velocity jitter: variance of speeds between consecutive points. Humans have high variance. */
  function jitterScore() {
    if (mouse.length < 10) return 0;
    var speeds = [];
    for (var i = 1; i < mouse.length; i++) {
      var dx = mouse[i].x - mouse[i - 1].x;
      var dy = mouse[i].y - mouse[i - 1].y;
      var dt = mouse[i].t - mouse[i - 1].t;
      if (dt > 0) speeds.push(Math.sqrt(dx * dx + dy * dy) / dt);
    }
    var v = variance(speeds);
    // High variance = human, low = bot
    if (v > 0.5) return 25;
    if (v > 0.1) return 18;
    if (v > 0.02) return 10;
    return 2;
  }

  /** Scroll smoothness: humans decelerate, bots jump instantly. */
  function scrollScore() {
    if (scrolls.length < 3) return 0;
    var deltas = [];
    for (var i = 1; i < scrolls.length; i++) {
      var dy = Math.abs(scrolls[i].y - scrolls[i - 1].y);
      var dt = scrolls[i].t - scrolls[i - 1].t;
      if (dt > 0) deltas.push(dy / dt);
    }
    var v = variance(deltas);
    if (v > 0.3) return 25;
    if (v > 0.05) return 18;
    if (v > 0.005) return 10;
    return 2;
  }

  /** Keystroke rhythm: variance of inter-key intervals. Humans are irregular. */
  function keyScore() {
    if (keys.length < 4) return 0;
    var intervals = [];
    for (var i = 1; i < keys.length; i++) {
      intervals.push(keys[i].t - keys[i - 1].t);
    }
    var v = variance(intervals);
    // Humans: high variance (thinking, pausing). Bots: near-constant.
    if (v > 10000) return 25;
    if (v > 2000) return 18;
    if (v > 300) return 10;
    return 2;
  }

  /** Touch pattern score (mobile). Humans have variable duration and slight swipe curves. */
  function touchScore() {
    if (touches.length < 2) return 0;
    var durs = [];
    for (var i = 0; i < touches.length; i++) durs.push(touches[i].dur);
    var v = variance(durs);
    if (v > 5000) return 25;
    if (v > 1000) return 18;
    if (v > 100) return 10;
    return 2;
  }

  // ── Compute final score ──

  function computeScore() {
    var curves   = curveScore();
    var jitter   = jitterScore();
    var smooth   = scrollScore();
    var keyVar   = keyScore();
    var touchVar = touchScore();

    // Time on page bonus: bots submit fast
    var elapsed = (Date.now() - startTs) / 1000;
    var timeBonus = 0;
    if (elapsed > 3) timeBonus = 5;
    if (elapsed > 8) timeBonus = 10;
    if (elapsed > 20) timeBonus = 15;

    // At least one input channel must have data
    var channels = 0;
    if (mouse.length >= 10) channels++;
    if (scrolls.length >= 3) channels++;
    if (keys.length >= 4) channels++;
    if (touches.length >= 2) channels++;

    // No data at all = likely bot (or JS disabled, but then shield doesn't run)
    if (channels === 0) return 5;

    var raw = curves + jitter + smooth + keyVar + touchVar + timeBonus;
    return clamp(Math.round(raw), 0, 100);
  }

  function buildToken() {
    var score = computeScore();
    var payload = {
      s: score,
      t: Date.now(),
      m: {
        c: curveScore(),
        j: jitterScore(),
        sc: scrollScore(),
        k: keyScore(),
        tc: touchScore(),
        pts: mouse.length,
        el: Math.round((Date.now() - startTs) / 1000)
      },
      v: VERSION
    };
    try {
      return btoa(JSON.stringify(payload));
    } catch (e) {
      return btoa('{"s":' + score + ',"v":"' + VERSION + '"}');
    }
  }

  // ── Form integration ──

  function injectField(form) {
    if (form.querySelector('input[name="' + FIELD_NAME + '"]')) return;
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = FIELD_NAME;
    input.value = '';
    form.appendChild(input);
  }

  function handleSubmit(e) {
    var form = e.target;
    if (!form || form.tagName !== 'FORM') return;

    var field = form.querySelector('input[name="' + FIELD_NAME + '"]');
    if (!field) {
      injectField(form);
      field = form.querySelector('input[name="' + FIELD_NAME + '"]');
    }

    var token = buildToken();
    field.value = token;

    // Decode score to check threshold
    var score = 0;
    try {
      var decoded = JSON.parse(atob(token));
      score = decoded.s || 0;
    } catch (err) {
      score = 0;
    }

    if (score < BLOCK_SCORE) {
      e.preventDefault();
      e.stopImmediatePropagation();
      // Log blocked attempt to backend
      try {
        var logPayload = JSON.stringify({
          event: 'shield_blocked',
          score: score,
          token: token,
          page: window.location.pathname,
          ua: navigator.userAgent,
          ts: new Date().toISOString()
        });
        navigator.sendBeacon && navigator.sendBeacon(
          'https://app.lingograde.com/api/shield-log', logPayload
        );
      } catch (logErr) { /* silent */ }
      // Generic message — don't reveal detection
      var msg = form.querySelector('.shield-msg');
      if (!msg) {
        msg = document.createElement('div');
        msg.className = 'shield-msg';
        msg.style.cssText = 'color:#c0392b;font-size:14px;margin-top:10px;font-family:Arial,sans-serif;';
        form.appendChild(msg);
      }
      msg.textContent = 'Something went wrong. Please try again.';
      // Reset collectors to give real users a second chance
      mouse = []; scrolls = []; keys = []; touches = [];
      startTs = Date.now();
      return false;
    }

    // Score 30-60: flag but allow
    if (score < FLAG_SCORE) {
      var flagField = form.querySelector('input[name="_shield_flag"]');
      if (!flagField) {
        flagField = document.createElement('input');
        flagField.type = 'hidden';
        flagField.name = '_shield_flag';
        form.appendChild(flagField);
      }
      flagField.value = 'suspicious';
    }
  }

  // ── Init ──

  function init() {
    // Attach event listeners
    document.addEventListener('mousemove', onMouse, { passive: true });
    document.addEventListener('scroll', onScroll, { passive: true });
    document.addEventListener('keydown', onKey, { passive: true });
    document.addEventListener('touchstart', onTouchStart, { passive: true });
    document.addEventListener('touchend', onTouchEnd, { passive: true });

    // Inject hidden fields into all existing forms
    var forms = document.querySelectorAll('form');
    for (var i = 0; i < forms.length; i++) {
      injectField(forms[i]);
    }

    // Listen for form submissions
    document.addEventListener('submit', handleSubmit, true);

    // Watch for dynamically added forms
    if (typeof MutationObserver !== 'undefined') {
      var observer = new MutationObserver(function (mutations) {
        for (var i = 0; i < mutations.length; i++) {
          var nodes = mutations[i].addedNodes;
          for (var j = 0; j < nodes.length; j++) {
            if (nodes[j].tagName === 'FORM') injectField(nodes[j]);
            if (nodes[j].querySelectorAll) {
              var nested = nodes[j].querySelectorAll('form');
              for (var k = 0; k < nested.length; k++) injectField(nested[k]);
            }
          }
        }
      });
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
