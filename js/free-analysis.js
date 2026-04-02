/**
 * LingoGrade Free Analysis v1.0
 * Handles language grid, text input, speech, rate limiting, and API submission.
 * Depends on: shield.js (bot detection)
 */
;(function () {
  'use strict';

  var API_URL = 'https://app.lingograde.com/api/free-analysis';
  var EMAIL_URL = 'https://app.lingograde.com/api/free-analysis/email';
  var MAX_ANALYSES = 3;
  var STORAGE_KEY = 'lg_fa_count';
  var MIN_CHARS = 50;

  // ── Language grid (same 28 as marco-chat.js) ──
  var LANGS = [
    { label: 'English', code: 'en' },
    { label: 'Deutsch', code: 'de' },
    { label: 'Fran\u00e7ais', code: 'fr' },
    { label: 'Espa\u00f1ol', code: 'es' },
    { label: 'Italiano', code: 'it' },
    { label: '\u0420\u0443\u0441\u0441\u043a\u0438\u0439', code: 'ru' },
    { label: '\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430', code: 'uk' },
    { label: '\u4e2d\u6587', code: 'zh' },
    { label: '\u0627\u0644\u0639\u0631\u0628\u064a\u0629', code: 'ar' },
    { label: 'T\u00fcrk\u00e7e', code: 'tr' },
    { label: 'Portugu\u00eas', code: 'pt' },
    { label: 'Polski', code: 'pl' },
    { label: 'Magyar', code: 'hu' },
    { label: 'Rom\u00e2n\u0103', code: 'ro' },
    { label: '\u0411\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438', code: 'bg' },
    { label: 'Srpski', code: 'sr' },
    { label: 'Hrvatski', code: 'hr' },
    { label: 'Shqip', code: 'sq' },
    { label: 'Nederlands', code: 'nl' },
    { label: 'Svenska', code: 'sv' },
    { label: 'Norsk', code: 'no' },
    { label: 'Dansk', code: 'da' },
    { label: 'Suomi', code: 'fi' },
    { label: '\u65e5\u672c\u8a9e', code: 'ja' },
    { label: '\ud55c\uad6d\uc5b4', code: 'ko' },
    { label: '\u0939\u093f\u0928\u094d\u0926\u0940', code: 'hi' },
    { label: '\u0641\u0627\u0631\u0633\u06cc', code: 'fa' },
    { label: '\u0540\u0561\u0575\u0565\u0580\u0565\u0576', code: 'hy' }
  ];

  var selectedLang = null;
  var lastCefr = null;
  var recognition = null;
  var isRecording = false;

  // ── DOM refs ──
  var grid = document.getElementById('fa-lang-grid');
  var textarea = document.getElementById('fa-text');
  var charCount = document.getElementById('fa-char-count');
  var micBtn = document.getElementById('fa-mic');
  var submitBtn = document.getElementById('fa-submit');
  var card = document.getElementById('fa-card');
  var loading = document.getElementById('fa-loading');
  var results = document.getElementById('fa-results');
  var cefrBadge = document.getElementById('fa-cefr-badge');
  var summary = document.getElementById('fa-summary');
  var strengthsList = document.getElementById('fa-strengths-list');
  var focusList = document.getElementById('fa-focus-list');
  var emailInput = document.getElementById('fa-email');
  var emailSave = document.getElementById('fa-email-save');
  var emailThanks = document.getElementById('fa-email-thanks');
  var rateLimitDiv = document.getElementById('fa-rate-limit');
  var hpField = document.getElementById('fa-hp-field');

  // ── Build language grid ──
  LANGS.forEach(function (lang) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'fa-lang-btn';
    btn.textContent = lang.label;
    btn.dataset.code = lang.code;
    btn.addEventListener('click', function () {
      document.querySelectorAll('.fa-lang-btn').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      selectedLang = lang.code;
      updateSubmitState();
    });
    grid.appendChild(btn);
  });

  // ── Character counter ──
  textarea.addEventListener('input', function () {
    var len = textarea.value.length;
    charCount.textContent = len + ' / 2000';
    charCount.className = 'fa-char-count';
    if (len > 0 && len < MIN_CHARS) charCount.classList.add('warn');
    else if (len >= MIN_CHARS) charCount.classList.add('ok');
    updateSubmitState();
  });

  // ── Submit button state ──
  function updateSubmitState() {
    var len = textarea.value.trim().length;
    submitBtn.disabled = !(selectedLang && len >= MIN_CHARS);
  }

  // ── Text quality check ──
  function isGarbageText(text) {
    if (text.length < MIN_CHARS) return true;
    // Check for repeated characters (e.g., "aaaaaaa...")
    var unique = new Set(text.replace(/\s/g, '').split(''));
    if (unique.size < 5) return true;
    // Check for repeated words
    var words = text.trim().split(/\s+/);
    if (words.length > 3) {
      var wordSet = new Set(words.map(function (w) { return w.toLowerCase(); }));
      if (wordSet.size <= 2) return true;
    }
    return false;
  }

  // ── Rate limiting ──
  function getCount() {
    try {
      var data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      var today = new Date().toISOString().slice(0, 10);
      if (data.date !== today) return 0;
      return data.count || 0;
    } catch (e) { return 0; }
  }

  function incrementCount() {
    try {
      var today = new Date().toISOString().slice(0, 10);
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ date: today, count: getCount() + 1 }));
    } catch (e) {}
  }

  function checkRateLimit() {
    if (getCount() >= MAX_ANALYSES) {
      card.style.display = 'none';
      loading.classList.remove('visible');
      results.classList.remove('visible');
      rateLimitDiv.classList.add('visible');
      return true;
    }
    return false;
  }

  // ── Speech Recognition ──
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    micBtn.style.display = 'flex';
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    var silenceTimer = null;

    var preRecordingText = '';

    recognition.onresult = function (e) {
      clearTimeout(silenceTimer);
      var transcript = '';
      for (var i = 0; i < e.results.length; i++) {
        transcript += e.results[i][0].transcript;
      }
      textarea.value = preRecordingText + (preRecordingText ? ' ' : '') + transcript;
      textarea.dispatchEvent(new Event('input'));

      // Auto-stop after 60s of silence
      silenceTimer = setTimeout(function () { stopRecording(); }, 60000);
    };

    recognition.onerror = function () { stopRecording(); };
    recognition.onend = function () { stopRecording(); };

    micBtn.addEventListener('click', function () {
      if (isRecording) {
        stopRecording();
      } else {
        startRecording();
      }
    });
  }

  function startRecording() {
    if (!recognition) return;
    preRecordingText = textarea.value;
    // Set language for recognition if selected
    if (selectedLang) {
      var langMap = { en: 'en-US', de: 'de-DE', fr: 'fr-FR', es: 'es-ES', it: 'it-IT', ru: 'ru-RU', uk: 'uk-UA', zh: 'zh-CN', ar: 'ar-SA', tr: 'tr-TR', pt: 'pt-PT', pl: 'pl-PL', hu: 'hu-HU', ro: 'ro-RO', bg: 'bg-BG', sr: 'sr-RS', hr: 'hr-HR', sq: 'sq-AL', nl: 'nl-NL', sv: 'sv-SE', no: 'nb-NO', da: 'da-DK', fi: 'fi-FI', ja: 'ja-JP', ko: 'ko-KR', hi: 'hi-IN', fa: 'fa-IR', hy: 'hy-AM' };
      recognition.lang = langMap[selectedLang] || selectedLang;
    }
    isRecording = true;
    micBtn.classList.add('recording');
    try { recognition.start(); } catch (e) {}
  }

  function stopRecording() {
    isRecording = false;
    micBtn.classList.remove('recording');
    try { recognition.stop(); } catch (e) {}
  }

  // ── Check rate limit on load ──
  checkRateLimit();

  // ── Submit handler ──
  submitBtn.addEventListener('click', function () {
    if (submitBtn.disabled) return;
    if (checkRateLimit()) return;

    var text = textarea.value.trim();

    // Honeypot check
    if (hpField.value) return;

    // Quality check
    if (isGarbageText(text)) {
      alert('Please write at least 50 characters of real text so Marco can give you a proper snapshot.');
      return;
    }

    // Get shield score — shield.js injects token on form submit
    var shieldScore = null;
    try {
      // Trigger shield by creating a temporary form and submitting it
      var tmpForm = document.createElement('form');
      tmpForm.style.cssText = 'position:absolute;left:-9999px';
      document.body.appendChild(tmpForm);
      tmpForm.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      var shieldField = tmpForm.querySelector('input[name="_shield"]');
      if (shieldField && shieldField.value) {
        var decoded = JSON.parse(atob(shieldField.value));
        shieldScore = decoded.s || null;
      }
      document.body.removeChild(tmpForm);
    } catch (e) {}

    // Show loading
    card.style.display = 'none';
    loading.classList.add('visible');
    results.classList.remove('visible');

    // API call
    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        language: selectedLang,
        shield_score: shieldScore,
        _hp_field: hpField.value || undefined
      })
    })
    .then(function (res) {
      if (!res.ok) throw new Error('API error: ' + res.status);
      return res.json();
    })
    .then(function (data) {
      incrementCount();
      showResults(data);
    })
    .catch(function (err) {
      loading.classList.remove('visible');
      card.style.display = 'block';
      alert('Something went wrong. Please try again in a moment.');
      console.error('Free analysis error:', err);
    });
  });

  // ── Render results ──
  function showResults(data) {
    loading.classList.remove('visible');
    results.classList.add('visible');

    lastCefr = data.cefr || null;
    cefrBadge.textContent = data.cefr || '?';
    summary.textContent = data.summary || '';

    strengthsList.innerHTML = '';
    (data.strengths || []).forEach(function (s) {
      var div = document.createElement('div');
      div.className = 'fa-item strength';
      div.innerHTML = '<div class="fa-item-dot"></div><p>' + escapeHtml(s) + '</p>';
      strengthsList.appendChild(div);
    });

    focusList.innerHTML = '';
    (data.focus_areas || []).forEach(function (f) {
      var div = document.createElement('div');
      div.className = 'fa-item focus';
      div.innerHTML = '<div class="fa-item-dot"></div><p>' + escapeHtml(f) + '</p>';
      focusList.appendChild(div);
    });

    // Scroll results into view
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // ── Email capture ──
  emailSave.addEventListener('click', function () {
    var email = emailInput.value.trim();
    if (!email || !email.includes('@')) return;

    emailSave.disabled = true;
    fetch(EMAIL_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, language: selectedLang, cefr: lastCefr })
    }).then(function (res) {
      if (!res.ok) throw new Error();
      emailInput.style.display = 'none';
      emailSave.style.display = 'none';
      emailThanks.style.display = 'block';
    }).catch(function () {
      emailSave.disabled = false;
      emailThanks.style.display = 'block';
      emailThanks.textContent = 'Something went wrong — try again.';
      emailThanks.style.color = '#e74c3c';
      setTimeout(function () { emailThanks.style.display = 'none'; }, 3000);
    });
  });
})();
