/**
 * Marco Chat Widget v2.0 — LingoGrade AI Assistant
 *
 * Floating chat widget powered by Marco the owl.
 * Self-initializing: include <script src="js/marco-chat.js" defer></script>
 *
 * v2.0: Browser language detection + language preference prompt.
 * Zero dependencies.
 */
;(function () {
  'use strict';

  var API = 'https://app.lingograde.com/api/chat';
  var STORE_KEY = 'marco_session';
  var LANG_KEY = 'marco_lang';
  var MASCOT = 'assets/mascot/marco-hero-tea-mugprint.png';
  var OWL = '\uD83E\uDD89'; // fallback emoji

  // ── Language greetings map ──
  var GREETINGS = {
    en: 'Hi! How can we help you today?',
    de: 'Hallo! Wie k\u00F6nnen wir dir heute helfen?',
    fr: 'Bonjour! Comment pouvons-nous vous aider?',
    es: '\u00A1Hola! \u00BFC\u00F3mo podemos ayudarte?',
    it: 'Ciao! Come possiamo aiutarti?',
    ru: '\u041F\u0440\u0438\u0432\u0435\u0442! \u0427\u0435\u043C \u043C\u044B \u043C\u043E\u0436\u0435\u043C \u043F\u043E\u043C\u043E\u0447\u044C?',
    uk: '\u041F\u0440\u0438\u0432\u0456\u0442! \u0427\u0438\u043C \u043C\u0438 \u043C\u043E\u0436\u0435\u043C\u043E \u0434\u043E\u043F\u043E\u043C\u043E\u0433\u0442\u0438?',
    zh: '\u4F60\u597D\uFF01\u6211\u4EEC\u80FD\u5E2E\u4F60\u4EC0\u4E48\uFF1F',
    ar: '\u0645\u0631\u062D\u0628\u0627\u064B! \u0643\u064A\u0641 \u064A\u0645\u0643\u0646\u0646\u0627 \u0645\u0633\u0627\u0639\u062F\u062A\u0643\u061F',
    tr: 'Merhaba! Size nas\u0131l yard\u0131mc\u0131 olabiliriz?',
    pt: 'Ol\u00E1! Como podemos ajud\u00E1-lo?',
    pl: 'Cze\u015B\u0107! Jak mo\u017Cemy ci pom\u00F3c?',
    hy: '\u0555\u0572\u057B\u0578\u0582\u0576! \u053B\u0576\u0579\u057A\u0565\u057D \u056F\u0561\u0580\u0578\u0572 \u0565\u0576\u0584 \u0585\u0563\u0576\u0565\u056C?',
    bg: '\u0417\u0434\u0440\u0430\u0432\u0435\u0439\u0442\u0435! \u041A\u0430\u043A \u043C\u043E\u0436\u0435\u043C \u0434\u0430 \u0432\u0438 \u043F\u043E\u043C\u043E\u0433\u043D\u0435\u043C?',
    sq: 'P\u00EBrsh\u00EBndetje! Si mund t\'ju ndihm\u00EBjm\u00EB?',
    ro: 'Bun\u0103! Cum v\u0103 putem ajuta?',
    hu: 'Szia! Miben seg\u00EDthet\u00FCnk?',
    hr: 'Bok! Kako vam mo\u017Eemo pomo\u0107i?',
    sr: '\u0417\u0434\u0440\u0430\u0432\u043E! \u041A\u0430\u043A\u043E \u0432\u0430\u043C \u043C\u043E\u0436\u0435\u043C\u043E \u043F\u043E\u043C\u043E\u045B\u0438?'
  };

  // ── Quick-select language buttons ──
  var LANG_BUTTONS = [
    { code: 'en', label: 'English' },
    { code: 'de', label: 'Deutsch' },
    { code: 'fr', label: 'Fran\u00E7ais' },
    { code: 'es', label: 'Espa\u00F1ol' },
    { code: 'it', label: 'Italiano' },
    { code: 'ru', label: '\u0420\u0443\u0441\u0441\u043A\u0438\u0439' },
    { code: 'zh', label: '\u4E2D\u6587' },
    { code: 'ar', label: '\u0627\u0644\u0639\u0631\u0628\u064A\u0629' },
    { code: 'tr', label: 'T\u00FCrk\u00E7e' },
    { code: 'pt', label: 'Portugu\u00EAs' },
    { code: 'pl', label: 'Polski' },
    { code: 'uk', label: '\u0423\u043A\u0440\u0430\u0457\u043D\u0441\u044C\u043A\u0430' }
  ];

  // ── Detect browser language (2-letter code) ──
  function detectLang() {
    var raw = (navigator.languages && navigator.languages[0]) || navigator.language || 'en';
    return raw.split('-')[0].toLowerCase();
  }

  // ── Get saved language preference ──
  function getSavedLang() {
    return localStorage.getItem(LANG_KEY);
  }

  function saveLang(code) {
    localStorage.setItem(LANG_KEY, code);
  }

  // ── Session ──
  function getSession() {
    var s = localStorage.getItem(STORE_KEY);
    if (s) return s;
    s = 'mc_' + Math.random().toString(36).slice(2) + Date.now().toString(36);
    localStorage.setItem(STORE_KEY, s);
    return s;
  }

  // ── Image loader with fallback ──
  function loadAvatar(el) {
    var img = new Image();
    img.onload = function () {
      el.style.backgroundImage = 'url(' + MASCOT + ')';
      el.style.backgroundSize = 'cover';
      el.style.backgroundPosition = 'center';
      el.textContent = '';
    };
    img.onerror = function () {
      el.textContent = OWL;
      el.style.fontSize = '28px';
      el.style.lineHeight = '60px';
      el.style.textAlign = 'center';
    };
    img.src = MASCOT;
  }

  // ── Inject styles ──
  var css = document.createElement('style');
  css.textContent = [
    '#marco-fab{position:fixed;bottom:24px;right:24px;width:60px;height:60px;border-radius:50%;',
    'background:#2563AB;color:#fff;border:none;cursor:pointer;z-index:9999;box-shadow:0 4px 16px rgba(0,0,0,.25);',
    'display:flex;align-items:center;justify-content:center;transition:transform .2s,box-shadow .2s}',
    '#marco-fab:hover{transform:scale(1.08);box-shadow:0 6px 24px rgba(0,0,0,.3)}',
    '#marco-chat{position:fixed;bottom:96px;right:24px;width:350px;height:500px;border-radius:16px;',
    'background:#fff;box-shadow:0 8px 40px rgba(0,0,0,.18);z-index:9998;display:none;flex-direction:column;',
    'overflow:hidden;font-family:"DM Sans",-apple-system,sans-serif}',
    '#marco-chat.open{display:flex}',
    '#marco-chat .mc-hdr{background:#2563AB;color:#fff;padding:14px 16px;display:flex;align-items:center;gap:10px;flex-shrink:0}',
    '#marco-chat .mc-hdr .mc-av{width:36px;height:36px;border-radius:50%;background:#1a4f8a;flex-shrink:0;',
    'display:flex;align-items:center;justify-content:center;overflow:hidden}',
    '#marco-chat .mc-hdr .mc-title{font-weight:600;font-size:.95rem;flex:1}',
    '#marco-chat .mc-hdr button{background:none;border:none;color:#fff;font-size:1.3rem;cursor:pointer;padding:0 4px;line-height:1}',
    '#marco-chat .mc-msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px}',
    '#marco-chat .mc-msg{max-width:85%;padding:10px 14px;border-radius:14px;font-size:.875rem;line-height:1.5;word-wrap:break-word}',
    '#marco-chat .mc-msg.bot{background:#EFF6FF;color:#1C1C1C;align-self:flex-start;border-bottom-left-radius:4px}',
    '#marco-chat .mc-msg.usr{background:#2563AB;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}',
    '#marco-chat .mc-msg.typing{background:#EFF6FF;align-self:flex-start;border-bottom-left-radius:4px}',
    '#marco-chat .mc-msg.typing span{display:inline-block;width:6px;height:6px;border-radius:50%;background:#8A8A8A;',
    'margin:0 2px;animation:mc-dot .6s ease-in-out infinite}',
    '#marco-chat .mc-msg.typing span:nth-child(2){animation-delay:.15s}',
    '#marco-chat .mc-msg.typing span:nth-child(3){animation-delay:.3s}',
    '@keyframes mc-dot{0%,80%,100%{opacity:.3;transform:scale(.8)}40%{opacity:1;transform:scale(1)}}',
    '#marco-chat .mc-input{display:flex;gap:8px;padding:12px 16px;border-top:1px solid #E0E0E0;flex-shrink:0}',
    '#marco-chat .mc-input input{flex:1;border:1px solid #E0E0E0;border-radius:24px;padding:8px 16px;font-size:.875rem;',
    'font-family:inherit;outline:none;transition:border-color .15s}',
    '#marco-chat .mc-input input:focus{border-color:#2563AB}',
    '#marco-chat .mc-input button{width:36px;height:36px;border-radius:50%;background:#2563AB;color:#fff;border:none;',
    'cursor:pointer;font-size:1.1rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background .15s}',
    '#marco-chat .mc-input button:hover{background:#1a4f8a}',
    '#marco-chat .mc-input button:disabled{background:#ccc;cursor:not-allowed}',
    // Language selector styles
    '#marco-chat .mc-lang-picker{align-self:flex-start;max-width:100%;display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}',
    '#marco-chat .mc-lang-picker button{padding:6px 12px;border-radius:20px;border:1.5px solid #2563AB;background:#fff;',
    'color:#1A3A5C;font-size:.8rem;font-family:inherit;cursor:pointer;transition:all .15s;font-weight:500;white-space:nowrap}',
    '#marco-chat .mc-lang-picker button:hover{background:#2563AB;color:#fff}',
    '#marco-chat .mc-lang-picker button.mc-other{border-color:#1A3A5C;color:#1A3A5C;background:transparent}',
    '#marco-chat .mc-lang-picker button.mc-other:hover{background:#1A3A5C;color:#fff}',
    '@media(max-width:480px){',
    '#marco-chat{bottom:0;right:0;left:0;width:100%;height:100%;border-radius:0}',
    '#marco-fab{bottom:16px;right:16px}',
    '}'
  ].join('\n');
  document.head.appendChild(css);

  // ── Build DOM ──
  var fab = document.createElement('button');
  fab.id = 'marco-fab';
  fab.setAttribute('aria-label', 'Chat with Marco');
  loadAvatar(fab);

  var chat = document.createElement('div');
  chat.id = 'marco-chat';
  chat.innerHTML = [
    '<div class="mc-hdr">',
    '  <div class="mc-av"></div>',
    '  <div class="mc-title">Ask Marco</div>',
    '  <button class="mc-min" aria-label="Minimize">&minus;</button>',
    '  <button class="mc-close" aria-label="Close">&times;</button>',
    '</div>',
    '<div class="mc-msgs"></div>',
    '<div class="mc-input">',
    '  <input type="text" placeholder="Ask me anything..." aria-label="Message">',
    '  <button aria-label="Send">&uarr;</button>',
    '</div>'
  ].join('');

  document.body.appendChild(fab);
  document.body.appendChild(chat);

  // Load avatar into header too
  var hdrAv = chat.querySelector('.mc-av');
  loadAvatar(hdrAv);

  var msgs = chat.querySelector('.mc-msgs');
  var input = chat.querySelector('.mc-input input');
  var sendBtn = chat.querySelector('.mc-input button');
  var isOpen = false;
  var sending = false;
  var chosenLang = getSavedLang();

  // ── Add a chat message (text only) ──
  function addMsg(type, text) {
    var el = document.createElement('div');
    el.className = 'mc-msg ' + type;
    el.textContent = text;
    msgs.appendChild(el);
    msgs.scrollTop = msgs.scrollHeight;
    return el;
  }

  // ── Add a chat message with HTML content ──
  function addMsgHtml(type, html) {
    var el = document.createElement('div');
    el.className = 'mc-msg ' + type;
    el.innerHTML = html;
    msgs.appendChild(el);
    msgs.scrollTop = msgs.scrollHeight;
    return el;
  }

  // ── Language picker ──
  function showLanguagePicker() {
    var browserLang = detectLang();
    var greeting = GREETINGS[browserLang] || GREETINGS.en;

    // Show detected-language greeting + English fallback
    var greetingText = greeting;
    if (browserLang !== 'en') {
      greetingText = greeting + '\n\n' + GREETINGS.en;
    }
    addMsg('bot', greetingText);

    // Prompt: in which language would you like to chat?
    var promptText = 'In which language would you like to chat?';
    if (browserLang !== 'en') {
      var prompts = {
        de: 'In welcher Sprache m\u00F6chtest du chatten?',
        fr: 'Dans quelle langue souhaitez-vous discuter?',
        es: '\u00BFEn qu\u00E9 idioma te gustar\u00EDa chatear?',
        it: 'In quale lingua vorresti chattare?',
        ru: '\u041D\u0430 \u043A\u0430\u043A\u043E\u043C \u044F\u0437\u044B\u043A\u0435 \u0432\u044B \u0445\u043E\u0442\u0438\u0442\u0435 \u043E\u0431\u0449\u0430\u0442\u044C\u0441\u044F?',
        uk: '\u042F\u043A\u043E\u044E \u043C\u043E\u0432\u043E\u044E \u0432\u0438 \u0445\u043E\u0447\u0435\u0442\u0435 \u0441\u043F\u0456\u043B\u043A\u0443\u0432\u0430\u0442\u0438\u0441\u044F?',
        zh: '\u60A8\u60F3\u7528\u54EA\u79CD\u8BED\u8A00\u804A\u5929\uFF1F',
        ar: '\u0628\u0623\u064A \u0644\u063A\u0629 \u062A\u0631\u064A\u062F \u0627\u0644\u062F\u0631\u062F\u0634\u0629\u061F',
        tr: 'Hangi dilde sohbet etmek istersiniz?',
        pt: 'Em qual idioma gostaria de conversar?',
        pl: 'W jakim j\u0119zyku chcesz rozmawia\u0107?',
        hy: '\u053B\u0576\u0579 \u056C\u0565\u0566\u0576\u0578\u057E \\u0565\u0584 \u0578\u0582\u0566\u0578\u0582\u043C \u0566\u0580\u0578\u0582\u0581\u0565\u056C?',
        bg: '\u041D\u0430 \u043A\u0430\u043A\u044A\u0432 \u0435\u0437\u0438\u043A \u0438\u0441\u043A\u0430\u0442\u0435 \u0434\u0430 \u0447\u0430\u0442\u0438\u0442\u0435?',
        sq: 'N\u00EB cil\u00EBn gjuh\u00EB doni t\u00EB bisedoni?',
        ro: '\u00CEn ce limb\u0103 dori\u021Bi s\u0103 conversa\u021Bi?',
        hu: 'Milyen nyelven szeretn\u00E9l besz\u00E9lgetni?',
        hr: 'Na kojem jeziku \u017Eelite razgovarati?',
        sr: '\u041D\u0430 \u043A\u043E\u043C \u0458\u0435\u0437\u0438\u043A\u0443 \u0436\u0435\u043B\u0438\u0442\u0435 \u0434\u0430 \u0440\u0430\u0437\u0433\u043E\u0432\u0430\u0440\u0430\u0442\u0435?'
      };
      var localPrompt = prompts[browserLang];
      if (localPrompt) {
        promptText = localPrompt + '\n' + promptText;
      }
    }
    addMsg('bot', promptText);

    // Build language buttons
    var picker = document.createElement('div');
    picker.className = 'mc-lang-picker';

    LANG_BUTTONS.forEach(function (lang) {
      var btn = document.createElement('button');
      btn.textContent = lang.label;
      btn.addEventListener('click', function () { selectLanguage(lang.code, lang.label, picker); });
      picker.appendChild(btn);
    });

    // "Other" button defaults to English
    var otherBtn = document.createElement('button');
    otherBtn.textContent = 'Other';
    otherBtn.className = 'mc-other';
    otherBtn.addEventListener('click', function () { selectLanguage('en', 'English', picker); });
    picker.appendChild(otherBtn);

    msgs.appendChild(picker);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function selectLanguage(code, label, pickerEl) {
    saveLang(code);
    chosenLang = code;

    // Remove picker buttons
    if (pickerEl && pickerEl.parentNode) {
      pickerEl.remove();
    }

    // Show user's selection as a user message
    addMsg('usr', label);

    // Greet in chosen language
    var greeting = GREETINGS[code] || GREETINGS.en;
    addMsg('bot', OWL + " " + greeting + "\n\nI'm Marco, LingoGrade's friendly owl. Ask me anything about our assessments, pricing, or how it all works!");
  }

  // ── Initial greeting logic ──
  function initGreeting() {
    if (chosenLang) {
      // Language already saved — greet directly
      var greeting = GREETINGS[chosenLang] || GREETINGS.en;
      addMsg('bot', OWL + " " + greeting + "\n\nI'm Marco, LingoGrade's friendly owl. Ask me anything about our assessments, pricing, or how it all works!");
    } else {
      // No preference yet — show language picker
      showLanguagePicker();
    }
  }

  initGreeting();

  // ── Events ──
  fab.addEventListener('click', function () { toggle(true); });
  chat.querySelector('.mc-min').addEventListener('click', function () { toggle(false); });
  chat.querySelector('.mc-close').addEventListener('click', function () { toggle(false); });

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  });
  sendBtn.addEventListener('click', send);

  function toggle(open) {
    isOpen = typeof open === 'boolean' ? open : !isOpen;
    chat.classList.toggle('open', isOpen);
    if (isOpen) input.focus();
  }

  function showTyping() {
    var el = document.createElement('div');
    el.className = 'mc-msg typing';
    el.innerHTML = '<span></span><span></span><span></span>';
    msgs.appendChild(el);
    msgs.scrollTop = msgs.scrollHeight;
    return el;
  }

  function send() {
    var text = input.value.trim();
    if (!text || sending) return;

    addMsg('usr', text);
    input.value = '';
    sending = true;
    sendBtn.disabled = true;

    var typing = showTyping();

    fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        session_id: getSession(),
        lang: chosenLang || detectLang()
      })
    })
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function (data) {
      typing.remove();
      addMsg('bot', data.response || 'Hmm, I got lost in my feathers. Try again?');
      if (data.session_id) localStorage.setItem(STORE_KEY, data.session_id);
    })
    .catch(function () {
      typing.remove();
      addMsg('bot', 'Oops, my nest lost signal. Please try again in a moment!');
    })
    .finally(function () {
      sending = false;
      sendBtn.disabled = false;
      input.focus();
    });
  }
})();
