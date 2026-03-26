/**
 * Marco Chat Widget v2.0 — LingoGrade AI Assistant
 *
 * Floating chat widget powered by Marco the owl.
 * Self-initializing: include <script src="js/marco-chat.js" defer></script>
 *
 * v2.0: Browser language detection + natural conversation language switch.
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

  // ── Language name → code mapping (matches names in any language) ──
  var LANG_NAMES = {
    // English names
    english: 'en', german: 'de', french: 'fr', spanish: 'es', italian: 'it',
    russian: 'ru', ukrainian: 'uk', chinese: 'zh', arabic: 'ar', turkish: 'tr',
    portuguese: 'pt', polish: 'pl', armenian: 'hy', bulgarian: 'bg',
    albanian: 'sq', romanian: 'ro', hungarian: 'hu', croatian: 'hr', serbian: 'sr',
    // Native names
    deutsch: 'de', 'français': 'fr', francais: 'fr', 'español': 'es', espanol: 'es',
    italiano: 'it', '\u0440\u0443\u0441\u0441\u043A\u0438\u0439': 'ru', '\u0443\u043A\u0440\u0430\u0457\u043D\u0441\u044C\u043A\u0430': 'uk',
    '\u4E2D\u6587': 'zh', '\u0627\u0644\u0639\u0631\u0628\u064A\u0629': 'ar', '\u062A\u0631\u06A9\u06CC': 'tr', 'türkçe': 'tr', turkce: 'tr',
    'português': 'pt', portugues: 'pt', polski: 'pl',
    '\u0570\u0561\u0575\u0565\u0580\u0565\u0576': 'hy', '\u0431\u044A\u043B\u0433\u0430\u0440\u0441\u043A\u0438': 'bg', shqip: 'sq',
    'română': 'ro', romana: 'ro', magyar: 'hu', hrvatski: 'hr',
    '\u0441\u0440\u043F\u0441\u043A\u0438': 'sr', srpski: 'sr',
    // French names
    allemand: 'de', anglais: 'en', espagnol: 'es', italien: 'it', russe: 'ru',
    chinois: 'zh', arabe: 'ar', turc: 'tr', portugais: 'pt', polonais: 'pl',
    // German names
    englisch: 'en', 'französisch': 'fr', franzosisch: 'fr',
    spanisch: 'es', italienisch: 'it', russisch: 'ru', chinesisch: 'zh',
    arabisch: 'ar', 'türkisch': 'tr', turkisch: 'tr', portugiesisch: 'pt',
    polnisch: 'pl', armenisch: 'hy', bulgarisch: 'bg', albanisch: 'sq',
    'rumänisch': 'ro', rumanisch: 'ro', ungarisch: 'hu', kroatisch: 'hr', serbisch: 'sr',
    // Spanish names
    'inglés': 'en', ingles: 'en', 'alemán': 'de', aleman: 'de', 'francés': 'fr', frances: 'fr',
    ruso: 'ru', chino: 'zh', 'árabe': 'ar', arabe: 'ar', turco: 'tr', 'portugués': 'pt',
    polaco: 'pl'
  };

  // ── Natural greeting messages per language ──
  var LANG_PROMPTS = {
    en: "Hi there! \uD83D\uDC4B\n\nI'm Marco, LingoGrade's friendly owl. Just type your preferred language and I'll switch automatically!\n\nExample: 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol', '\u4E2D\u6587'...",
    de: "Hallo! \uD83D\uDC4B\n\nIch habe bemerkt, dass dein Browser auf Deutsch eingestellt ist. M\u00F6chtest du auf Deutsch weitermachen, oder tippe einfach deine bevorzugte Sprache ein und ich wechsle automatisch!\n\nExample: 'English', 'Fran\u00E7ais', 'Espa\u00F1ol', '\u4E2D\u6587'...",
    fr: "Bonjour! \uD83D\uDC4B\n\nJ'ai remarqu\u00E9 que votre navigateur est en fran\u00E7ais. Voulez-vous continuer en fran\u00E7ais, ou tapez simplement votre langue pr\u00E9f\u00E9r\u00E9e et je changerai automatiquement!\n\nExample: 'English', 'Deutsch', 'Espa\u00F1ol', '\u4E2D\u6587'...",
    es: "\u00A1Hola! \uD83D\uDC4B\n\nHe notado que tu navegador est\u00E1 en espa\u00F1ol. \u00BFQuieres continuar en espa\u00F1ol, o simplemente escribe tu idioma preferido y cambiar\u00E9 autom\u00E1ticamente!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', '\u4E2D\u6587'...",
    it: "Ciao! \uD83D\uDC4B\n\nHo notato che il tuo browser \u00E8 in italiano. Vuoi continuare in italiano, o scrivi semplicemente la tua lingua preferita e cambier\u00F2 automaticamente!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    ru: "\u041F\u0440\u0438\u0432\u0435\u0442! \uD83D\uDC4B\n\n\u042F \u0437\u0430\u043C\u0435\u0442\u0438\u043B, \u0447\u0442\u043E \u0432\u0430\u0448 \u0431\u0440\u0430\u0443\u0437\u0435\u0440 \u043D\u0430\u0441\u0442\u0440\u043E\u0435\u043D \u043D\u0430 \u0440\u0443\u0441\u0441\u043A\u0438\u0439. \u0425\u043E\u0442\u0438\u0442\u0435 \u043F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u0442\u044C \u043D\u0430 \u0440\u0443\u0441\u0441\u043A\u043E\u043C, \u0438\u043B\u0438 \u043F\u0440\u043E\u0441\u0442\u043E \u043D\u0430\u043F\u0438\u0448\u0438\u0442\u0435 \u043F\u0440\u0435\u0434\u043F\u043E\u0447\u0438\u0442\u0430\u0435\u043C\u044B\u0439 \u044F\u0437\u044B\u043A!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    uk: "\u041F\u0440\u0438\u0432\u0456\u0442! \uD83D\uDC4B\n\n\u042F \u043F\u043E\u043C\u0456\u0442\u0438\u0432, \u0449\u043E \u0432\u0430\u0448 \u0431\u0440\u0430\u0443\u0437\u0435\u0440 \u043D\u0430\u043B\u0430\u0448\u0442\u043E\u0432\u0430\u043D\u0438\u0439 \u043D\u0430 \u0443\u043A\u0440\u0430\u0457\u043D\u0441\u044C\u043A\u0443. \u0425\u043E\u0447\u0435\u0442\u0435 \u043F\u0440\u043E\u0434\u043E\u0432\u0436\u0438\u0442\u0438 \u0443\u043A\u0440\u0430\u0457\u043D\u0441\u044C\u043A\u043E\u044E, \u0430\u0431\u043E \u043F\u0440\u043E\u0441\u0442\u043E \u043D\u0430\u043F\u0438\u0448\u0456\u0442\u044C \u0431\u0430\u0436\u0430\u043D\u0443 \u043C\u043E\u0432\u0443!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    zh: "\u4F60\u597D\uFF01\uD83D\uDC4B\n\n\u6211\u6CE8\u610F\u5230\u60A8\u7684\u6D4F\u89C8\u5668\u8BBE\u7F6E\u4E3A\u4E2D\u6587\u3002\u60A8\u60F3\u7EE7\u7EED\u4F7F\u7528\u4E2D\u6587\uFF0C\u8FD8\u662F\u8F93\u5165\u60A8\u559C\u6B22\u7684\u8BED\u8A00\uFF0C\u6211\u4F1A\u81EA\u52A8\u5207\u6362\uFF01\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    ar: "\u0645\u0631\u062D\u0628\u0627\u064B! \uD83D\uDC4B\n\n\u0644\u0627\u062D\u0638\u062A \u0623\u0646 \u0645\u062A\u0635\u0641\u062D\u0643 \u0645\u0636\u0628\u0648\u0637 \u0639\u0644\u0649 \u0627\u0644\u0639\u0631\u0628\u064A\u0629. \u0647\u0644 \u062A\u0631\u064A\u062F \u0627\u0644\u0645\u062A\u0627\u0628\u0639\u0629 \u0628\u0627\u0644\u0639\u0631\u0628\u064A\u0629\u060C \u0623\u0648 \u0627\u0643\u062A\u0628 \u0644\u063A\u062A\u0643 \u0627\u0644\u0645\u0641\u0636\u0644\u0629 \u0648\u0633\u0623\u063A\u064A\u0631 \u062A\u0644\u0642\u0627\u0626\u064A\u0627\u064B!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    tr: "Merhaba! \uD83D\uDC4B\n\nTaray\u0131c\u0131n\u0131z\u0131n T\u00FCrk\u00E7e oldu\u011Funu fark ettim. T\u00FCrk\u00E7e devam etmek ister misiniz, yoksa tercih etti\u011Finiz dili yaz\u0131n, otomatik ge\u00E7ey im!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    pt: "Ol\u00E1! \uD83D\uDC4B\n\nNotei que seu navegador est\u00E1 em portugu\u00EAs. Quer continuar em portugu\u00EAs, ou digite seu idioma preferido e eu mudo automaticamente!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    pl: "Cze\u015B\u0107! \uD83D\uDC4B\n\nZauwa\u017Cy\u0142em, \u017Ce Twoja przegl\u0105darka jest ustawiona na polski. Chcesz kontynuowa\u0107 po polsku, czy po prostu wpisz preferowany j\u0119zyk, a prze\u0142\u0105cz\u0119 si\u0119 automatycznie!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    hy: "\u0555\u0572\u057B\u0578\u0582\u0576! \uD83D\uDC4B\n\nI noticed your browser is set to Armenian. Would you like to continue in Armenian, or just type your preferred language below and I'll switch automatically!\n\nExample: 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol', '\u4E2D\u6587'...",
    bg: "\u0417\u0434\u0440\u0430\u0432\u0435\u0439\u0442\u0435! \uD83D\uDC4B\n\n\u0417\u0430\u0431\u0435\u043B\u044F\u0437\u0430\u0445, \u0447\u0435 \u0431\u0440\u0430\u0443\u0437\u044A\u0440\u044A\u0442 \u0432\u0438 \u0435 \u043D\u0430 \u0431\u044A\u043B\u0433\u0430\u0440\u0441\u043A\u0438. \u0418\u0441\u043A\u0430\u0442\u0435 \u043B\u0438 \u0434\u0430 \u043F\u0440\u043E\u0434\u044A\u043B\u0436\u0438\u0442\u0435 \u043D\u0430 \u0431\u044A\u043B\u0433\u0430\u0440\u0441\u043A\u0438, \u0438\u043B\u0438 \u043F\u0440\u043E\u0441\u0442\u043E \u043D\u0430\u043F\u0438\u0448\u0435\u0442\u0435 \u043F\u0440\u0435\u0434\u043F\u043E\u0447\u0438\u0442\u0430\u043D\u0438\u044F \u0435\u0437\u0438\u043A!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    sq: "P\u00EBrsh\u00EBndetje! \uD83D\uDC4B\n\nVura re q\u00EB shfletuesi juaj \u00EBsht\u00EB n\u00EB shqip. D\u00EBshironi t\u00EB vazhdoni n\u00EB shqip, apo thjesht shkruani gjuh\u00EBn tuaj t\u00EB preferuar!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    ro: "Bun\u0103! \uD83D\uDC4B\n\nAm observat c\u0103 browserul t\u0103u este \u00EEn rom\u00E2n\u0103. Vrei s\u0103 continui \u00EEn rom\u00E2n\u0103, sau scrie limba preferat\u0103 \u0219i schimb automat!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    hu: "Szia! \uD83D\uDC4B\n\n\u00C9szrevettem, hogy a b\u00F6ng\u00E9sz\u0151d magyarra van \u00E1ll\u00EDtva. Szeretn\u00E9l magyarul folytatni, vagy \u00EDrd be a k\u00EDv\u00E1nt nyelvet \u00E9s automatikusan v\u00E1ltok!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    hr: "Bok! \uD83D\uDC4B\n\nPrimijetio sam da je va\u0161 preglednik na hrvatskom. \u017Delite li nastaviti na hrvatskom, ili samo upi\u0161ite \u017Eeljeni jezik i automatski \u0107u se prebaciti!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'...",
    sr: "\u0417\u0434\u0440\u0430\u0432\u043E! \uD83D\uDC4B\n\n\u041F\u0440\u0438\u043C\u0435\u0442\u0438\u043E \u0441\u0430\u043C \u0434\u0430 \u0458\u0435 \u0432\u0430\u0448 \u043F\u0440\u0435\u0433\u043B\u0435\u0434\u0430\u0447 \u043D\u0430 \u0441\u0440\u043F\u0441\u043A\u043E\u043C. \u0416\u0435\u043B\u0438\u0442\u0435 \u043B\u0438 \u0434\u0430 \u043D\u0430\u0441\u0442\u0430\u0432\u0438\u0442\u0435 \u043D\u0430 \u0441\u0440\u043F\u0441\u043A\u043E\u043C, \u0438\u043B\u0438 \u0441\u0430\u043C\u043E \u0443\u043A\u0443\u0446\u0430\u0458\u0442\u0435 \u0436\u0435\u0459\u0435\u043D\u0438 \u0458\u0435\u0437\u0438\u043A!\n\nExample: 'English', 'Deutsch', 'Fran\u00E7ais', 'Espa\u00F1ol'..."
  };

  // ── Detect language from user text input ──
  function detectLangFromText(text) {
    var normalized = text.trim().toLowerCase();
    // Direct match
    if (LANG_NAMES[normalized]) return LANG_NAMES[normalized];
    // Partial match (user typed e.g. "I want German" or just "german")
    var keys = Object.keys(LANG_NAMES);
    for (var i = 0; i < keys.length; i++) {
      if (normalized.indexOf(keys[i]) !== -1 || keys[i].indexOf(normalized) !== -1) {
        return LANG_NAMES[keys[i]];
      }
    }
    return null;
  }

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
    // (language picker buttons removed — natural text input used instead)
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

  // ── Natural language prompt (no buttons) ──
  var waitingForLang = false;

  function showLanguagePrompt() {
    var browserLang = detectLang();
    var prompt = LANG_PROMPTS[browserLang] || LANG_PROMPTS.en;
    addMsg('bot', prompt);
    waitingForLang = true;
  }

  function handleLangResponse(text) {
    var detected = detectLangFromText(text);
    // Also accept "yes", "ok", "sure", "da", "ja", "oui", "si" etc. as confirmation of browser language
    var confirmWords = ['yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'ja', 'oui', 'si', 'da', '\u0434\u0430', '\u0442\u0430\u043A', '\u0561\u0575\u043E', 'evet', 'sim', 'tak', '\u0434\u0430\u043A\u043B\u0435', 'po', 'igen', 'ano'];
    var normalized = text.trim().toLowerCase();
    if (!detected && confirmWords.indexOf(normalized) !== -1) {
      detected = detectLang();
    }
    if (detected) {
      saveLang(detected);
      chosenLang = detected;
      waitingForLang = false;
      var greeting = GREETINGS[detected] || GREETINGS.en;
      addMsg('bot', OWL + " " + greeting + "\n\nI'm Marco, LingoGrade's friendly owl. Ask me anything about our assessments, pricing, or how it all works!");
      return true;
    }
    // If we can't detect, default to browser language and proceed
    var fallback = detectLang();
    if (GREETINGS[fallback]) {
      saveLang(fallback);
      chosenLang = fallback;
    } else {
      saveLang('en');
      chosenLang = 'en';
    }
    waitingForLang = false;
    var g = GREETINGS[chosenLang] || GREETINGS.en;
    addMsg('bot', OWL + " " + g + "\n\nI'm Marco, LingoGrade's friendly owl. Ask me anything about our assessments, pricing, or how it all works!");
    return false; // message was not a language selection — will be sent as regular message
  }

  // ── Initial greeting logic ──
  function initGreeting() {
    if (chosenLang) {
      // Language already saved — greet directly
      var greeting = GREETINGS[chosenLang] || GREETINGS.en;
      addMsg('bot', OWL + " " + greeting + "\n\nI'm Marco, LingoGrade's friendly owl. Ask me anything about our assessments, pricing, or how it all works!");
    } else {
      // No preference yet — show natural language prompt
      showLanguagePrompt();
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

    // Intercept if we're waiting for language selection
    if (waitingForLang) {
      addMsg('usr', text);
      input.value = '';
      var wasLang = handleLangResponse(text);
      if (wasLang) return; // language was detected, greeting shown, done
      // Not a recognizable language — already set fallback, now send as regular message
    } else {
      addMsg('usr', text);
      input.value = '';
    }

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
