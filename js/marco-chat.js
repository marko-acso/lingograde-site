/**
 * Marco Chat Widget v3.0 — LingoGrade AI Assistant
 *
 * Floating chat widget powered by Marco the owl.
 * Self-initializing: include <script src="js/marco-chat.js" defer></script>
 *
 * v3.0: Click-to-select language grid + optional email capture.
 * Zero dependencies.
 */
;(function () {
  'use strict';

  var API = 'https://app.lingograde.com/api/chat';
  var STORE_KEY = 'marco_session';
  var LANG_KEY = 'marco_lang';
  var EMAIL_KEY = 'marco_email';
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
    hu: 'Szia! Miben seg\u00EDthet\u00FCnk?',
    ro: 'Bun\u0103! Cum v\u0103 putem ajuta?',
    bg: '\u0417\u0434\u0440\u0430\u0432\u0435\u0439\u0442\u0435! \u041A\u0430\u043A \u043C\u043E\u0436\u0435\u043C \u0434\u0430 \u0432\u0438 \u043F\u043E\u043C\u043E\u0433\u043D\u0435\u043C?',
    sr: '\u0417\u0434\u0440\u0430\u0432\u043E! \u041A\u0430\u043A\u043E \u0432\u0430\u043C \u043C\u043E\u0436\u0435\u043C\u043E \u043F\u043E\u043C\u043E\u045B\u0438?',
    hr: 'Bok! Kako vam mo\u017Eemo pomo\u0107i?',
    sq: 'P\u00EBrsh\u00EBndetje! Si mund t\'ju ndihm\u00EBjm\u00EB?',
    hy: '\u0555\u0572\u057B\u0578\u0582\u0576! \u053B\u0576\u0579\u057A\u0565\u057D \u056F\u0561\u0580\u0578\u0572 \u0565\u0576\u0584 \u0585\u0563\u0576\u0565\u056C?',
    nl: 'Hallo! Hoe kunnen we je helpen?',
    sv: 'Hej! Hur kan vi hj\u00E4lpa dig?',
    no: 'Hei! Hvordan kan vi hjelpe deg?',
    da: 'Hej! Hvordan kan vi hj\u00E6lpe dig?',
    fi: 'Hei! Miten voimme auttaa?',
    ja: '\u3053\u3093\u306B\u3061\u306F\uFF01\u3069\u3046\u304A\u624B\u4F1D\u3044\u3057\u307E\u3057\u3087\u3046\u304B\uFF1F',
    ko: '\uC548\uB155\uD558\uC138\uC694! \uBB34\uC5C7\uC744 \uB3C4\uC640\uB4DC\uB9B4\uAE4C\uC694?',
    hi: '\u0928\u092E\u0938\u094D\u0924\u0947! \u0939\u092E \u0906\u092A\u0915\u0940 \u0915\u0948\u0938\u0947 \u092E\u0926\u0926 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902?',
    fa: '\u0633\u0644\u0627\u0645! \u0686\u0637\u0648\u0631 \u0645\u06CC\u200C\u062A\u0648\u0627\u0646\u06CC\u0645 \u06A9\u0645\u06A9\u062A\u0627\u0646 \u06A9\u0646\u06CC\u0645\u061F'
  };

  // ── Language grid: label → code ──
  var LANG_GRID = [
    { label: 'English',    code: 'en' },
    { label: 'Deutsch',    code: 'de' },
    { label: 'Fran\u00E7ais',  code: 'fr' },
    { label: 'Espa\u00F1ol',   code: 'es' },
    { label: 'Italiano',   code: 'it' },
    { label: '\u0420\u0443\u0441\u0441\u043A\u0438\u0439',  code: 'ru' },
    { label: '\u0423\u043A\u0440\u0430\u0457\u043D\u0441\u044C\u043A\u0430', code: 'uk' },
    { label: '\u4E2D\u6587',       code: 'zh' },
    { label: '\u0627\u0644\u0639\u0631\u0628\u064A\u0629',    code: 'ar' },
    { label: 'T\u00FCrk\u00E7e',   code: 'tr' },
    { label: 'Portugu\u00EAs', code: 'pt' },
    { label: 'Polski',    code: 'pl' },
    { label: 'Magyar',    code: 'hu' },
    { label: 'Rom\u00E2n\u0103',    code: 'ro' },
    { label: '\u0411\u044A\u043B\u0433\u0430\u0440\u0441\u043A\u0438', code: 'bg' },
    { label: 'Srpski',    code: 'sr' },
    { label: 'Hrvatski',  code: 'hr' },
    { label: 'Shqip',     code: 'sq' },
    { label: 'Nederlands', code: 'nl' },
    { label: 'Svenska',   code: 'sv' },
    { label: 'Norsk',     code: 'no' },
    { label: 'Dansk',     code: 'da' },
    { label: 'Suomi',     code: 'fi' },
    { label: '\u65E5\u672C\u8A9E',     code: 'ja' },
    { label: '\uD55C\uAD6D\uC5B4',     code: 'ko' },
    { label: '\u0939\u093F\u0928\u094D\u0926\u0940',     code: 'hi' },
    { label: '\u0641\u0627\u0631\u0633\u06CC',     code: 'fa' },
    { label: '\u0540\u0561\u0575\u0565\u0580\u0565\u0576',  code: 'hy' }
  ];

  // ── Greeting + confirm messages per language ──
  var CONFIRM_MSGS = {
    en: { greeting: 'Hi! \uD83D\uDC4B', question: 'Shall we continue in English?', yes: 'Yes, continue in English', no: 'Choose another language' },
    de: { greeting: 'Hallo! \uD83D\uDC4B', question: 'Sollen wir auf Deutsch weitermachen?', yes: 'Ja, weiter auf Deutsch', no: 'Andere Sprache w\u00E4hlen' },
    fr: { greeting: 'Bonjour! \uD83D\uDC4B', question: 'On continue en fran\u00E7ais?', yes: 'Oui, continuer en fran\u00E7ais', no: 'Choisir une autre langue' },
    es: { greeting: '\u00A1Hola! \uD83D\uDC4B', question: '\u00BFSeguimos en espa\u00F1ol?', yes: 'S\u00ED, seguir en espa\u00F1ol', no: 'Elegir otro idioma' },
    it: { greeting: 'Ciao! \uD83D\uDC4B', question: 'Continuiamo in italiano?', yes: 'S\u00EC, continua in italiano', no: 'Scegli un\'altra lingua' },
    ru: { greeting: '\u041F\u0440\u0438\u0432\u0435\u0442! \uD83D\uDC4B', question: '\u041F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u043C \u043D\u0430 \u0440\u0443\u0441\u0441\u043A\u043E\u043C?', yes: '\u0414\u0430, \u043F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u0442\u044C \u043D\u0430 \u0440\u0443\u0441\u0441\u043A\u043E\u043C', no: '\u0412\u044B\u0431\u0440\u0430\u0442\u044C \u0434\u0440\u0443\u0433\u043E\u0439 \u044F\u0437\u044B\u043A' },
    uk: { greeting: '\u041F\u0440\u0438\u0432\u0456\u0442! \uD83D\uDC4B', question: '\u041F\u0440\u043E\u0434\u043E\u0432\u0436\u0438\u043C\u043E \u0443\u043A\u0440\u0430\u0457\u043D\u0441\u044C\u043A\u043E\u044E?', yes: '\u0422\u0430\u043A, \u043F\u0440\u043E\u0434\u043E\u0432\u0436\u0438\u0442\u0438 \u0443\u043A\u0440\u0430\u0457\u043D\u0441\u044C\u043A\u043E\u044E', no: '\u041E\u0431\u0440\u0430\u0442\u0438 \u0456\u043D\u0448\u0443 \u043C\u043E\u0432\u0443' },
    zh: { greeting: '\u4F60\u597D\uFF01\uD83D\uDC4B', question: '\u7EE7\u7EED\u4F7F\u7528\u4E2D\u6587\u5417\uFF1F', yes: '\u662F\u7684\uFF0C\u7EE7\u7EED\u4E2D\u6587', no: '\u9009\u62E9\u5176\u4ED6\u8BED\u8A00' },
    ar: { greeting: '\u0645\u0631\u062D\u0628\u0627\u064B! \uD83D\uDC4B', question: '\u0646\u0643\u0645\u0644 \u0628\u0627\u0644\u0639\u0631\u0628\u064A\u0629\u061F', yes: '\u0646\u0639\u0645\u060C \u0627\u0633\u062A\u0645\u0631 \u0628\u0627\u0644\u0639\u0631\u0628\u064A\u0629', no: '\u0627\u062E\u062A\u0631 \u0644\u063A\u0629 \u0623\u062E\u0631\u0649' },
    tr: { greeting: 'Merhaba! \uD83D\uDC4B', question: 'T\u00FCrk\u00E7e devam edelim mi?', yes: 'Evet, T\u00FCrk\u00E7e devam', no: 'Ba\u015Fka dil se\u00E7' },
    pt: { greeting: 'Ol\u00E1! \uD83D\uDC4B', question: 'Continuamos em portugu\u00EAs?', yes: 'Sim, continuar em portugu\u00EAs', no: 'Escolher outro idioma' },
    pl: { greeting: 'Cze\u015B\u0107! \uD83D\uDC4B', question: 'Kontynuujemy po polsku?', yes: 'Tak, kontynuuj po polsku', no: 'Wybierz inny j\u0119zyk' }
  };

  // ── Email prompt messages per language ──
  var EMAIL_MSGS = {
    en: { prompt: 'Before we start \u2014 would you like to leave your email so Marco can follow up if we get disconnected? (optional)', placeholder: 'your@email.com', skip: 'Skip', cont: 'Continue', helper: 'This helps Marco remember you next time' },
    de: { prompt: 'Bevor wir starten \u2014 m\u00F6chtest du deine E-Mail hinterlassen, damit Marco dich wiederfinden kann, falls die Verbindung abbricht? (optional)', placeholder: 'deine@email.de', skip: '\u00DCberspringen', cont: 'Weiter', helper: 'So kann Marco dich beim n\u00E4chsten Mal wiedererkennen' },
    fr: { prompt: 'Avant de commencer \u2014 voulez-vous laisser votre email pour que Marco puisse vous recontacter en cas de d\u00E9connexion? (optionnel)', placeholder: 'votre@email.fr', skip: 'Passer', cont: 'Continuer', helper: 'Cela aide Marco \u00E0 se souvenir de vous' },
    es: { prompt: 'Antes de empezar \u2014 \u00BFquieres dejar tu email para que Marco pueda contactarte si se corta la conexi\u00F3n? (opcional)', placeholder: 'tu@email.es', skip: 'Saltar', cont: 'Continuar', helper: 'Esto ayuda a Marco a recordarte la pr\u00F3xima vez' },
    it: { prompt: 'Prima di iniziare \u2014 vuoi lasciare la tua email cos\u00EC Marco pu\u00F2 ricontattarti se perdiamo la connessione? (opzionale)', placeholder: 'tua@email.it', skip: 'Salta', cont: 'Continua', helper: 'Questo aiuta Marco a ricordarti la prossima volta' },
    ru: { prompt: '\u041F\u0440\u0435\u0436\u0434\u0435 \u0447\u0435\u043C \u043D\u0430\u0447\u0430\u0442\u044C \u2014 \u0445\u043E\u0442\u0438\u0442\u0435 \u043E\u0441\u0442\u0430\u0432\u0438\u0442\u044C email, \u0447\u0442\u043E\u0431\u044B \u041C\u0430\u0440\u043A\u043E \u043C\u043E\u0433 \u0441\u0432\u044F\u0437\u0430\u0442\u044C\u0441\u044F \u0441 \u0432\u0430\u043C\u0438? (\u043D\u0435\u043E\u0431\u044F\u0437\u0430\u0442\u0435\u043B\u044C\u043D\u043E)', placeholder: 'your@email.com', skip: '\u041F\u0440\u043E\u043F\u0443\u0441\u0442\u0438\u0442\u044C', cont: '\u041F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u0442\u044C', helper: '\u042D\u0442\u043E \u043F\u043E\u043C\u043E\u0436\u0435\u0442 \u041C\u0430\u0440\u043A\u043E \u0437\u0430\u043F\u043E\u043C\u043D\u0438\u0442\u044C \u0432\u0430\u0441' }
  };

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
    '#marco-chat{position:fixed;bottom:96px;right:24px;width:370px;height:520px;border-radius:16px;',
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
    // Language confirm buttons
    '.mc-confirm-btns{display:flex;flex-direction:column;gap:6px;margin-top:8px}',
    '.mc-confirm-btns button{padding:8px 14px;border-radius:10px;border:1.5px solid #2563AB;background:#fff;color:#2563AB;',
    'font-size:.82rem;font-family:inherit;cursor:pointer;transition:all .15s;text-align:center}',
    '.mc-confirm-btns button:hover{background:#2563AB;color:#fff}',
    '.mc-confirm-btns button.mc-btn-primary{background:#2563AB;color:#fff}',
    '.mc-confirm-btns button.mc-btn-primary:hover{background:#1a4f8a}',
    // Language grid
    '.mc-lang-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-top:8px;max-height:240px;overflow-y:auto;padding-right:4px}',
    '.mc-lang-grid button{padding:6px 4px;border-radius:8px;border:1px solid #D1D5DB;background:#fff;color:#1C1C1C;',
    'font-size:.78rem;font-family:inherit;cursor:pointer;transition:all .15s;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.mc-lang-grid button:hover{background:#2563AB;color:#fff;border-color:#2563AB}',
    // Email capture
    '.mc-email-block{display:flex;flex-direction:column;gap:6px;margin-top:8px}',
    '.mc-email-block input{border:1px solid #D1D5DB;border-radius:10px;padding:8px 12px;font-size:.82rem;font-family:inherit;outline:none}',
    '.mc-email-block input:focus{border-color:#2563AB}',
    '.mc-email-block .mc-email-helper{font-size:.72rem;color:#6B7280;margin-top:-2px}',
    '.mc-email-block .mc-email-btns{display:flex;gap:6px}',
    '.mc-email-block .mc-email-btns button{flex:1;padding:7px 10px;border-radius:10px;border:1.5px solid #2563AB;',
    'font-size:.82rem;font-family:inherit;cursor:pointer;transition:all .15s;text-align:center}',
    '.mc-email-block .mc-email-btns .mc-btn-skip{background:#fff;color:#6B7280;border-color:#D1D5DB}',
    '.mc-email-block .mc-email-btns .mc-btn-skip:hover{background:#F3F4F6}',
    '.mc-email-block .mc-email-btns .mc-btn-cont{background:#2563AB;color:#fff}',
    '.mc-email-block .mc-email-btns .mc-btn-cont:hover{background:#1a4f8a}',
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
  var inputArea = chat.querySelector('.mc-input');
  var input = chat.querySelector('.mc-input input');
  var sendBtn = chat.querySelector('.mc-input button');
  var isOpen = false;
  var sending = false;
  var chosenLang = getSavedLang();
  var flowPhase = 'idle'; // idle | lang-confirm | lang-grid | email | chat

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

  // ── Disable/enable text input during flow phases ──
  function setInputEnabled(enabled) {
    input.disabled = !enabled;
    sendBtn.disabled = !enabled;
    if (enabled) {
      input.placeholder = 'Ask me anything...';
    } else {
      input.placeholder = '';
    }
  }

  // ── Step 1: Show greeting + confirm/switch buttons ──
  function showLangConfirm() {
    flowPhase = 'lang-confirm';
    setInputEnabled(false);
    var browserLang = detectLang();
    var msgs_ = CONFIRM_MSGS[browserLang] || CONFIRM_MSGS.en;
    var yesLabel = msgs_.yes;
    var noLabel = msgs_.no;

    var el = addMsgHtml('bot',
      msgs_.greeting + ' ' + msgs_.question +
      '<div class="mc-confirm-btns">' +
      '<button class="mc-btn-primary" data-action="confirm-lang" data-lang="' + browserLang + '">' + yesLabel + '</button>' +
      '<button data-action="switch-lang">' + noLabel + '</button>' +
      '</div>'
    );

    el.querySelector('[data-action="confirm-lang"]').addEventListener('click', function () {
      var lang = this.getAttribute('data-lang');
      disableButtons(el);
      addMsg('usr', yesLabel);
      selectLanguage(lang);
    });

    el.querySelector('[data-action="switch-lang"]').addEventListener('click', function () {
      disableButtons(el);
      addMsg('usr', noLabel);
      showLangGrid();
    });
  }

  // ── Step 2 (optional): Show language grid ──
  function showLangGrid() {
    flowPhase = 'lang-grid';
    setInputEnabled(false);
    var html = '<div class="mc-lang-grid">';
    for (var i = 0; i < LANG_GRID.length; i++) {
      html += '<button data-lang="' + LANG_GRID[i].code + '">' + LANG_GRID[i].label + '</button>';
    }
    html += '</div>';

    var el = addMsgHtml('bot', html);
    var buttons = el.querySelectorAll('.mc-lang-grid button');
    for (var j = 0; j < buttons.length; j++) {
      buttons[j].addEventListener('click', function () {
        var lang = this.getAttribute('data-lang');
        var label = this.textContent;
        disableButtons(el);
        addMsg('usr', label);
        selectLanguage(lang);
      });
    }
  }

  // ── Step 3: Language selected → ask for email ──
  function selectLanguage(code) {
    saveLang(code);
    chosenLang = code;
    showEmailCapture();
  }

  // ── Step 4: Email capture (optional) ──
  function showEmailCapture() {
    flowPhase = 'email';
    setInputEnabled(false);
    var lang = chosenLang || 'en';
    var em = EMAIL_MSGS[lang] || EMAIL_MSGS.en;

    var html = em.prompt +
      '<div class="mc-email-block">' +
      '<input type="email" placeholder="' + em.placeholder + '" class="mc-email-input">' +
      '<div class="mc-email-helper">' + em.helper + '</div>' +
      '<div class="mc-email-btns">' +
      '<button class="mc-btn-skip" data-action="email-skip">' + em.skip + '</button>' +
      '<button class="mc-btn-cont" data-action="email-cont">' + em.cont + '</button>' +
      '</div></div>';

    var el = addMsgHtml('bot', html);

    var emailInput = el.querySelector('.mc-email-input');
    var skipBtn = el.querySelector('[data-action="email-skip"]');
    var contBtn = el.querySelector('[data-action="email-cont"]');

    skipBtn.addEventListener('click', function () {
      disableButtons(el);
      emailInput.disabled = true;
      addMsg('usr', em.skip);
      startConversation();
    });

    contBtn.addEventListener('click', function () {
      var email = emailInput.value.trim();
      if (email && email.indexOf('@') !== -1) {
        localStorage.setItem(EMAIL_KEY, email);
        disableButtons(el);
        emailInput.disabled = true;
        addMsg('usr', email);
        startConversation();
      } else if (!email) {
        // Treat empty as skip
        disableButtons(el);
        emailInput.disabled = true;
        addMsg('usr', em.skip);
        startConversation();
      } else {
        emailInput.style.borderColor = '#EF4444';
        emailInput.focus();
      }
    });

    emailInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        contBtn.click();
      }
    });
  }

  // ── Step 5: Start actual conversation ──
  function startConversation() {
    flowPhase = 'chat';
    setInputEnabled(true);
    var greeting = GREETINGS[chosenLang] || GREETINGS.en;
    addMsg('bot', OWL + " " + greeting + "\n\nI'm Marco, LingoGrade's friendly owl. Ask me anything about our assessments, pricing, or how it all works!");
    input.focus();
  }

  // ── Utility: disable all buttons inside an element after click ──
  function disableButtons(el) {
    var btns = el.querySelectorAll('button');
    for (var i = 0; i < btns.length; i++) {
      btns[i].disabled = true;
      btns[i].style.opacity = '0.5';
      btns[i].style.cursor = 'default';
    }
  }

  // ── Initial greeting logic ──
  function initGreeting() {
    if (chosenLang) {
      // Language already saved — go straight to conversation
      flowPhase = 'chat';
      setInputEnabled(true);
      var greeting = GREETINGS[chosenLang] || GREETINGS.en;
      addMsg('bot', OWL + " " + greeting + "\n\nI'm Marco, LingoGrade's friendly owl. Ask me anything about our assessments, pricing, or how it all works!");
    } else {
      // No preference yet — show language confirm flow
      showLangConfirm();
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
    if (isOpen && flowPhase === 'chat') input.focus();
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
    if (!text || sending || flowPhase !== 'chat') return;

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
        lang: chosenLang || detectLang(),
        email: localStorage.getItem(EMAIL_KEY) || undefined
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
