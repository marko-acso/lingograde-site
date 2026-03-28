/**
 * Marco Chat Widget v3.0 — LingoGrade AI Assistant
 *
 * Floating chat widget powered by Marco the owl.
 * Self-initializing: include <script src="js/marco-chat.js" defer></script>
 *
 * v3.0: Click-to-select language grid + optional email capture.
 * v4.0: Conversational sales flow with personalized assessment offers.
 * Zero dependencies.
 */
;(function () {
  'use strict';

  var API = 'https://app.lingograde.com/api/chat';
  var STORE_KEY = 'marco_session';
  var LANG_KEY = 'marco_lang';
  var EMAIL_KEY = 'marco_email';
  var MASCOT = 'assets/mascot/marco-headset.png';
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
    pl: { greeting: 'Cze\u015B\u0107! \uD83D\uDC4B', question: 'Kontynuujemy po polsku?', yes: 'Tak, kontynuuj po polsku', no: 'Wybierz inny j\u0119zyk' },
    hu: { greeting: 'Szia! \uD83D\uDC4B', question: 'Folytatjuk magyarul?', yes: 'Igen, folytatom magyarul', no: 'V\u00E1lasszon m\u00E1sik nyelvet' },
    ro: { greeting: 'Bun\u0103! \uD83D\uDC4B', question: 'Continu\u0103m \u00EEn rom\u00E2n\u0103?', yes: 'Da, continu\u0103 \u00EEn rom\u00E2n\u0103', no: 'Alege\u021Bi alt\u0103 limb\u0103' },
    bg: { greeting: '\u0417\u0434\u0440\u0430\u0432\u0435\u0439\u0442\u0435! \uD83D\uDC4B', question: '\u041F\u0440\u043E\u0434\u044A\u043B\u0436\u0430\u0432\u0430\u043C\u0435 \u043D\u0430 \u0431\u044A\u043B\u0433\u0430\u0440\u0441\u043A\u0438?', yes: '\u0414\u0430, \u043F\u0440\u043E\u0434\u044A\u043B\u0436\u0438 \u043D\u0430 \u0431\u044A\u043B\u0433\u0430\u0440\u0441\u043A\u0438', no: '\u0418\u0437\u0431\u0435\u0440\u0435\u0442\u0435 \u0434\u0440\u0443\u0433 \u0435\u0437\u0438\u043A' },
    sr: { greeting: '\u0417\u0434\u0440\u0430\u0432\u043E! \uD83D\uDC4B', question: '\u041D\u0430\u0441\u0442\u0430\u0432\u043B\u044F\u043C\u043E \u043D\u0430 \u0441\u0440\u043F\u0441\u043A\u043E\u043C?', yes: '\u0414\u0430, \u043D\u0430\u0441\u0442\u0430\u0432\u0438 \u043D\u0430 \u0441\u0440\u043F\u0441\u043A\u043E\u043C', no: '\u0418\u0437\u0430\u0431\u0435\u0440\u0438\u0442\u0435 \u0434\u0440\u0443\u0433\u0438 \u0458\u0435\u0437\u0438\u043A' },
    hr: { greeting: 'Bok! \uD83D\uDC4B', question: 'Nastavljamo na hrvatskom?', yes: 'Da, nastavi na hrvatskom', no: 'Odaberite drugi jezik' },
    sq: { greeting: 'P\u00EBrsh\u00EBndetje! \uD83D\uDC4B', question: 'Vazhdojm\u00EB n\u00EB shqip?', yes: 'Po, vazhdo n\u00EB shqip', no: 'Zgjidhni nj\u00EB gjuh\u00EB tjet\u00EBr' },
    hy: { greeting: '\u0555\u0572\u057B\u0578\u0582\u0576! \uD83D\uDC4B', question: '\u0547\u0561\u0580\u0578\u0582\u0576\u0561\u056F\u0565\u0576\u0584 \u0570\u0561\u0575\u0565\u0580\u0565\u0576\u0578\u057E?', yes: '\u0531\u0575\u0578, \u0577\u0561\u0580\u0578\u0582\u0576\u0561\u056F\u0565\u056C \u0570\u0561\u0575\u0565\u0580\u0565\u0576\u0578\u057E', no: '\u0538\u0576\u057F\u0580\u0565\u056C \u0561\u0575\u056C \u056C\u0565\u0566\u0578\u0582' },
    nl: { greeting: 'Hallo! \uD83D\uDC4B', question: 'Gaan we verder in het Nederlands?', yes: 'Ja, ga verder in het Nederlands', no: 'Kies een andere taal' },
    sv: { greeting: 'Hej! \uD83D\uDC4B', question: 'Forts\u00E4tter vi p\u00E5 svenska?', yes: 'Ja, forts\u00E4tt p\u00E5 svenska', no: 'V\u00E4lj ett annat spr\u00E5k' },
    no: { greeting: 'Hei! \uD83D\uDC4B', question: 'Fortsetter vi p\u00E5 norsk?', yes: 'Ja, fortsett p\u00E5 norsk', no: 'Velg et annet spr\u00E5k' },
    da: { greeting: 'Hej! \uD83D\uDC4B', question: 'Forts\u00E6tter vi p\u00E5 dansk?', yes: 'Ja, forts\u00E6t p\u00E5 dansk', no: 'V\u00E6lg et andet sprog' },
    fi: { greeting: 'Hei! \uD83D\uDC4B', question: 'Jatketaanko suomeksi?', yes: 'Kyll\u00E4, jatka suomeksi', no: 'Valitse toinen kieli' },
    ja: { greeting: '\u3053\u3093\u306B\u3061\u306F\uFF01\uD83D\uDC4B', question: '\u65E5\u672C\u8A9E\u3067\u7D9A\u3051\u307E\u3057\u3087\u3046\u304B\uFF1F', yes: '\u306F\u3044\u3001\u65E5\u672C\u8A9E\u3067\u7D9A\u3051\u308B', no: '\u4ED6\u306E\u8A00\u8A9E\u3092\u9078\u3076' },
    ko: { greeting: '\uC548\uB155\uD558\uC138\uC694! \uD83D\uDC4B', question: '\uD55C\uAD6D\uC5B4\uB85C \uACC4\uC18D\uD560\uAE4C\uC694?', yes: '\uB124, \uD55C\uAD6D\uC5B4\uB85C \uACC4\uC18D', no: '\uB2E4\uB978 \uC5B8\uC5B4 \uC120\uD0DD' },
    hi: { greeting: '\u0928\u092E\u0938\u094D\u0924\u0947! \uD83D\uDC4B', question: '\u0939\u093F\u0928\u094D\u0926\u0940 \u092E\u0947\u0902 \u091C\u093E\u0930\u0940 \u0930\u0916\u0947\u0902?', yes: '\u0939\u093E\u0901, \u0939\u093F\u0928\u094D\u0926\u0940 \u092E\u0947\u0902 \u091C\u093E\u0930\u0940 \u0930\u0916\u0947\u0902', no: '\u0926\u0942\u0938\u0930\u0940 \u092D\u093E\u0937\u093E \u091A\u0941\u0928\u0947\u0902' },
    fa: { greeting: '\u0633\u0644\u0627\u0645! \uD83D\uDC4B', question: '\u0628\u0647 \u0641\u0627\u0631\u0633\u06CC \u0627\u062F\u0627\u0645\u0647 \u0628\u062F\u0647\u06CC\u0645\u061F', yes: '\u0628\u0644\u0647\u060C \u0628\u0647 \u0641\u0627\u0631\u0633\u06CC \u0627\u062F\u0627\u0645\u0647 \u0628\u062F\u0647', no: '\u0627\u0646\u062A\u062E\u0627\u0628 \u0632\u0628\u0627\u0646 \u062F\u06CC\u06AF\u0631' }
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

  // ── Sales flow translations (en, de, fr, es, it, ru, zh) ──
  var SALES_MSGS = {
    en: {
      intentQ: "So, are you here to check your language level, or just curious about what we do?",
      checkLevel: "Check my level",
      justLooking: "Just looking around",
      whichLang: "Which language are you learning?",
      howLong: "How long have you been learning {lang}?",
      duration: ["Just started", "6 months - 1 year", "1-3 years", "3+ years"],
      challengeQ: "What's your biggest challenge?",
      challenges: ["Speaking", "Grammar", "Vocabulary", "Confidence", "Everything \uD83D\uDE05"],
      recommend: "Based on what you told me, I think a {pkg} would be perfect for you.",
      voss: "Would it be crazy to find out your real level in just {time}?",
      bookNow: "Book Now",
      emailOffer: "Want me to send the details to your email?",
      lookingReply: "No worries! I'm here whenever you're ready. Here's what people usually ask about:",
      faqBtns: ["How does it work?", "What does it cost?", "Is it online?", "How fast do I get results?"],
      faqAnswers: [
        "You book a session, talk with Marco for 15-40 minutes, and get a full CEFR report with personalized homework. It's like a friendly chat, not a scary exam!",
        "We have packages from \u20AC69.95 (15 min quick assessment) to \u20AC249.95 (40 min deep analysis). Every package includes a detailed CEFR report.",
        "100% online! You just need a microphone and an internet connection. Book a time that works for you.",
        "You'll get your full report within 24 hours after your session. Most people get it within a few hours!"
      ],
      faqCta: "Want to try it?",
      exitEmail: "Before you go \u2014 want Marco to send you a summary? Drop your email and I'll follow up with something useful.",
      exitSend: "Send",
      exitSkip: "No thanks",
      emailThanks: "Got it! I'll send you something useful soon. \uD83E\uDD89",
      readyAnytime: "I'm here whenever you need me!"
    },
    de: {
      intentQ: "Und, bist du hier, um dein Sprachniveau zu checken, oder einfach neugierig, was wir machen?",
      checkLevel: "Mein Niveau checken",
      justLooking: "Nur mal schauen",
      whichLang: "Welche Sprache lernst du?",
      howLong: "Wie lange lernst du schon {lang}?",
      duration: ["Gerade angefangen", "6 Monate - 1 Jahr", "1-3 Jahre", "3+ Jahre"],
      challengeQ: "Was ist deine gr\u00F6\u00DFte Herausforderung?",
      challenges: ["Sprechen", "Grammatik", "Wortschatz", "Selbstvertrauen", "Alles \uD83D\uDE05"],
      recommend: "Nach dem, was du mir erz\u00E4hlt hast, w\u00E4re ein {pkg} perfekt f\u00FCr dich.",
      voss: "W\u00E4re es verr\u00FCckt, dein echtes Niveau in nur {time} herauszufinden?",
      bookNow: "Jetzt buchen",
      emailOffer: "Soll ich dir die Details per E-Mail schicken?",
      lookingReply: "Kein Problem! Ich bin hier, wenn du bereit bist. Hier ist, was die Leute meistens fragen:",
      faqBtns: ["Wie funktioniert es?", "Was kostet es?", "Ist es online?", "Wie schnell bekomme ich Ergebnisse?"],
      faqAnswers: [
        "Du buchst eine Session, sprichst 15-40 Minuten mit Marco und bekommst einen vollst\u00E4ndigen CEFR-Bericht mit personalisierten Haus\u00FCbungen. Wie ein freundliches Gespr\u00E4ch, keine Pr\u00FCfung!",
        "Wir haben Pakete von \u20AC69.95 (15 Min. Schnell-Check) bis \u20AC249.95 (40 Min. Tiefenanalyse). Jedes Paket enth\u00E4lt einen detaillierten CEFR-Bericht.",
        "100% online! Du brauchst nur ein Mikrofon und eine Internetverbindung. Buche eine Zeit, die dir passt.",
        "Du bekommst deinen Bericht innerhalb von 24 Stunden. Die meisten bekommen ihn schon nach wenigen Stunden!"
      ],
      faqCta: "Willst du es ausprobieren?",
      exitEmail: "Bevor du gehst \u2014 soll Marco dir eine Zusammenfassung schicken? Hinterlass deine E-Mail und ich melde mich mit etwas N\u00FCtzlichem.",
      exitSend: "Senden",
      exitSkip: "Nein danke",
      emailThanks: "Hab's! Ich schicke dir bald etwas N\u00FCtzliches. \uD83E\uDD89",
      readyAnytime: "Ich bin hier, wann immer du mich brauchst!"
    },
    fr: {
      intentQ: "Alors, tu es l\u00E0 pour v\u00E9rifier ton niveau de langue, ou juste curieux de ce qu'on fait?",
      checkLevel: "V\u00E9rifier mon niveau",
      justLooking: "Je regarde juste",
      whichLang: "Quelle langue apprends-tu?",
      howLong: "Depuis combien de temps apprends-tu {lang}?",
      duration: ["Je viens de commencer", "6 mois - 1 an", "1-3 ans", "3+ ans"],
      challengeQ: "Quel est ton plus grand d\u00E9fi?",
      challenges: ["Parler", "Grammaire", "Vocabulaire", "Confiance", "Tout \uD83D\uDE05"],
      recommend: "D'apr\u00E8s ce que tu m'as dit, je pense qu'un {pkg} serait parfait pour toi.",
      voss: "Ce serait fou de d\u00E9couvrir ton vrai niveau en seulement {time}, non?",
      bookNow: "R\u00E9server",
      emailOffer: "Tu veux que je t'envoie les d\u00E9tails par email?",
      lookingReply: "Pas de souci! Je suis l\u00E0 quand tu es pr\u00EAt. Voici ce que les gens demandent g\u00E9n\u00E9ralement:",
      faqBtns: ["Comment \u00E7a marche?", "Combien \u00E7a co\u00FBte?", "C'est en ligne?", "En combien de temps j'ai les r\u00E9sultats?"],
      faqAnswers: [
        "Tu r\u00E9serves une session, tu parles avec Marco pendant 15-40 minutes, et tu re\u00E7ois un rapport CECR complet avec des devoirs personnalis\u00E9s. C'est une conversation amicale, pas un examen!",
        "On a des forfaits de 69.95\u20AC (15 min \u00E9valuation rapide) \u00E0 249.95\u20AC (40 min analyse approfondie). Chaque forfait inclut un rapport CECR d\u00E9taill\u00E9.",
        "100% en ligne! Tu as juste besoin d'un micro et d'une connexion internet. Choisis l'heure qui te convient.",
        "Tu recevras ton rapport dans les 24 heures. La plupart des gens le re\u00E7oivent en quelques heures!"
      ],
      faqCta: "Tu veux essayer?",
      exitEmail: "Avant de partir \u2014 tu veux que Marco t'envoie un r\u00E9sum\u00E9? Laisse ton email et je te recontacte avec quelque chose d'utile.",
      exitSend: "Envoyer",
      exitSkip: "Non merci",
      emailThanks: "Re\u00E7u! Je t'envoie quelque chose d'utile bient\u00F4t. \uD83E\uDD89",
      readyAnytime: "Je suis l\u00E0 quand tu as besoin de moi!"
    },
    es: {
      intentQ: "\u00BFVienes a comprobar tu nivel de idioma, o solo tienes curiosidad por lo que hacemos?",
      checkLevel: "Comprobar mi nivel",
      justLooking: "Solo estoy mirando",
      whichLang: "\u00BFQu\u00E9 idioma est\u00E1s aprendiendo?",
      howLong: "\u00BFCu\u00E1nto tiempo llevas aprendiendo {lang}?",
      duration: ["Acabo de empezar", "6 meses - 1 a\u00F1o", "1-3 a\u00F1os", "3+ a\u00F1os"],
      challengeQ: "\u00BFCu\u00E1l es tu mayor desaf\u00EDo?",
      challenges: ["Hablar", "Gram\u00E1tica", "Vocabulario", "Confianza", "Todo \uD83D\uDE05"],
      recommend: "Por lo que me cuentas, creo que un {pkg} ser\u00EDa perfecto para ti.",
      voss: "\u00BFSer\u00EDa una locura descubrir tu nivel real en solo {time}?",
      bookNow: "Reservar ahora",
      emailOffer: "\u00BFQuieres que te env\u00EDe los detalles por email?",
      lookingReply: "\u00A1Sin problema! Estoy aqu\u00ED cuando est\u00E9s listo. Esto es lo que la gente suele preguntar:",
      faqBtns: ["\u00BFC\u00F3mo funciona?", "\u00BFCu\u00E1nto cuesta?", "\u00BFEs online?", "\u00BFQu\u00E9 tan r\u00E1pido obtengo resultados?"],
      faqAnswers: [
        "Reservas una sesi\u00F3n, hablas con Marco durante 15-40 minutos y recibes un informe MCER completo con tareas personalizadas. \u00A1Es como una charla amigable, no un examen!",
        "Tenemos paquetes desde 69.95\u20AC (15 min evaluaci\u00F3n r\u00E1pida) hasta 249.95\u20AC (40 min an\u00E1lisis profundo). Cada paquete incluye un informe MCER detallado.",
        "\u00A1100% online! Solo necesitas un micr\u00F3fono y conexi\u00F3n a internet. Elige el horario que te convenga.",
        "\u00A1Recibir\u00E1s tu informe en 24 horas! La mayor\u00EDa lo recibe en pocas horas."
      ],
      faqCta: "\u00BFQuieres probarlo?",
      exitEmail: "Antes de irte \u2014 \u00BFquieres que Marco te env\u00EDe un resumen? Deja tu email y te escribo con algo \u00FAtil.",
      exitSend: "Enviar",
      exitSkip: "No gracias",
      emailThanks: "\u00A1Recibido! Te enviar\u00E9 algo \u00FAtil pronto. \uD83E\uDD89",
      readyAnytime: "\u00A1Estoy aqu\u00ED cuando me necesites!"
    },
    it: {
      intentQ: "Allora, sei qui per controllare il tuo livello linguistico, o semplicemente curioso di quello che facciamo?",
      checkLevel: "Controlla il mio livello",
      justLooking: "Sto solo guardando",
      whichLang: "Quale lingua stai imparando?",
      howLong: "Da quanto tempo stai imparando {lang}?",
      duration: ["Ho appena iniziato", "6 mesi - 1 anno", "1-3 anni", "3+ anni"],
      challengeQ: "Qual \u00E8 la tua sfida pi\u00F9 grande?",
      challenges: ["Parlare", "Grammatica", "Vocabolario", "Fiducia", "Tutto \uD83D\uDE05"],
      recommend: "In base a quello che mi hai detto, penso che un {pkg} sarebbe perfetto per te.",
      voss: "Sarebbe pazzesco scoprire il tuo vero livello in soli {time}?",
      bookNow: "Prenota ora",
      emailOffer: "Vuoi che ti invii i dettagli via email?",
      lookingReply: "Nessun problema! Sono qui quando sei pronto. Ecco cosa chiedono di solito:",
      faqBtns: ["Come funziona?", "Quanto costa?", "\u00C8 online?", "Quanto velocemente ottengo i risultati?"],
      faqAnswers: [
        "Prenoti una sessione, parli con Marco per 15-40 minuti e ricevi un rapporto QCER completo con compiti personalizzati. \u00C8 come una chiacchierata amichevole, non un esame!",
        "Abbiamo pacchetti da 69.95\u20AC (15 min valutazione rapida) a 249.95\u20AC (40 min analisi approfondita). Ogni pacchetto include un rapporto QCER dettagliato.",
        "100% online! Ti serve solo un microfono e una connessione internet. Scegli l'orario che ti va meglio.",
        "Riceverai il rapporto entro 24 ore. La maggior parte lo riceve in poche ore!"
      ],
      faqCta: "Vuoi provare?",
      exitEmail: "Prima di andare \u2014 vuoi che Marco ti invii un riepilogo? Lascia la tua email e ti scrivo qualcosa di utile.",
      exitSend: "Invia",
      exitSkip: "No grazie",
      emailThanks: "Ricevuto! Ti mando qualcosa di utile presto. \uD83E\uDD89",
      readyAnytime: "Sono qui quando hai bisogno di me!"
    },
    ru: {
      intentQ: "\u0418\u0442\u0430\u043A, \u0442\u044B \u0437\u0434\u0435\u0441\u044C, \u0447\u0442\u043E\u0431\u044B \u043F\u0440\u043E\u0432\u0435\u0440\u0438\u0442\u044C \u0441\u0432\u043E\u0439 \u0443\u0440\u043E\u0432\u0435\u043D\u044C \u044F\u0437\u044B\u043A\u0430, \u0438\u043B\u0438 \u043F\u0440\u043E\u0441\u0442\u043E \u0438\u043D\u0442\u0435\u0440\u0435\u0441\u043D\u043E, \u0447\u0435\u043C \u043C\u044B \u0437\u0430\u043D\u0438\u043C\u0430\u0435\u043C\u0441\u044F?",
      checkLevel: "\u041F\u0440\u043E\u0432\u0435\u0440\u0438\u0442\u044C \u043C\u043E\u0439 \u0443\u0440\u043E\u0432\u0435\u043D\u044C",
      justLooking: "\u041F\u0440\u043E\u0441\u0442\u043E \u0441\u043C\u043E\u0442\u0440\u044E",
      whichLang: "\u041A\u0430\u043A\u043E\u0439 \u044F\u0437\u044B\u043A \u0442\u044B \u0438\u0437\u0443\u0447\u0430\u0435\u0448\u044C?",
      howLong: "\u0421\u043A\u043E\u043B\u044C\u043A\u043E \u0432\u0440\u0435\u043C\u0435\u043D\u0438 \u0442\u044B \u0443\u0447\u0438\u0448\u044C {lang}?",
      duration: ["\u0422\u043E\u043B\u044C\u043A\u043E \u043D\u0430\u0447\u0430\u043B", "6 \u043C\u0435\u0441. - 1 \u0433\u043E\u0434", "1-3 \u0433\u043E\u0434\u0430", "3+ \u0433\u043E\u0434\u0430"],
      challengeQ: "\u0427\u0442\u043E \u0434\u043B\u044F \u0442\u0435\u0431\u044F \u0441\u0430\u043C\u043E\u0435 \u0441\u043B\u043E\u0436\u043D\u043E\u0435?",
      challenges: ["\u0420\u0430\u0437\u0433\u043E\u0432\u043E\u0440", "\u0413\u0440\u0430\u043C\u043C\u0430\u0442\u0438\u043A\u0430", "\u0421\u043B\u043E\u0432\u0430\u0440\u043D\u044B\u0439 \u0437\u0430\u043F\u0430\u0441", "\u0423\u0432\u0435\u0440\u0435\u043D\u043D\u043E\u0441\u0442\u044C", "\u0412\u0441\u0451 \uD83D\uDE05"],
      recommend: "\u0418\u0441\u0445\u043E\u0434\u044F \u0438\u0437 \u0442\u043E\u0433\u043E, \u0447\u0442\u043E \u0442\u044B \u0440\u0430\u0441\u0441\u043A\u0430\u0437\u0430\u043B, \u044F \u0434\u0443\u043C\u0430\u044E, {pkg} \u0431\u044B\u043B \u0431\u044B \u0438\u0434\u0435\u0430\u043B\u044C\u043D\u044B\u043C \u0434\u043B\u044F \u0442\u0435\u0431\u044F.",
      voss: "\u0411\u044B\u043B\u043E \u0431\u044B \u0431\u0435\u0437\u0443\u043C\u0438\u0435\u043C \u0443\u0437\u043D\u0430\u0442\u044C \u0441\u0432\u043E\u0439 \u0440\u0435\u0430\u043B\u044C\u043D\u044B\u0439 \u0443\u0440\u043E\u0432\u0435\u043D\u044C \u0432\u0441\u0435\u0433\u043E \u0437\u0430 {time}?",
      bookNow: "\u0417\u0430\u0431\u0440\u043E\u043D\u0438\u0440\u043E\u0432\u0430\u0442\u044C",
      emailOffer: "\u0425\u043E\u0447\u0435\u0448\u044C, \u0447\u0442\u043E\u0431\u044B \u044F \u043E\u0442\u043F\u0440\u0430\u0432\u0438\u043B \u0434\u0435\u0442\u0430\u043B\u0438 \u043D\u0430 \u0442\u0432\u043E\u0439 email?",
      lookingReply: "\u0411\u0435\u0437 \u043F\u0440\u043E\u0431\u043B\u0435\u043C! \u042F \u0437\u0434\u0435\u0441\u044C, \u043A\u043E\u0433\u0434\u0430 \u0431\u0443\u0434\u0435\u0448\u044C \u0433\u043E\u0442\u043E\u0432. \u0412\u043E\u0442 \u0447\u0442\u043E \u043E\u0431\u044B\u0447\u043D\u043E \u0441\u043F\u0440\u0430\u0448\u0438\u0432\u0430\u044E\u0442:",
      faqBtns: ["\u041A\u0430\u043A \u044D\u0442\u043E \u0440\u0430\u0431\u043E\u0442\u0430\u0435\u0442?", "\u0421\u043A\u043E\u043B\u044C\u043A\u043E \u0441\u0442\u043E\u0438\u0442?", "\u042D\u0442\u043E \u043E\u043D\u043B\u0430\u0439\u043D?", "\u041A\u0430\u043A \u0431\u044B\u0441\u0442\u0440\u043E \u043F\u0440\u0438\u0445\u043E\u0434\u044F\u0442 \u0440\u0435\u0437\u0443\u043B\u044C\u0442\u0430\u0442\u044B?"],
      faqAnswers: [
        "\u0422\u044B \u0431\u0440\u043E\u043D\u0438\u0440\u0443\u0435\u0448\u044C \u0441\u0435\u0441\u0441\u0438\u044E, \u0433\u043E\u0432\u043E\u0440\u0438\u0448\u044C \u0441 \u041C\u0430\u0440\u043A\u043E 15-40 \u043C\u0438\u043D\u0443\u0442 \u0438 \u043F\u043E\u043B\u0443\u0447\u0430\u0435\u0448\u044C \u043F\u043E\u043B\u043D\u044B\u0439 \u043E\u0442\u0447\u0451\u0442 CEFR \u0441 \u043F\u0435\u0440\u0441\u043E\u043D\u0430\u043B\u044C\u043D\u044B\u043C \u0434\u043E\u043C\u0430\u0448\u043D\u0438\u043C \u0437\u0430\u0434\u0430\u043D\u0438\u0435\u043C. \u042D\u0442\u043E \u043A\u0430\u043A \u0434\u0440\u0443\u0436\u0435\u0441\u043A\u0438\u0439 \u0440\u0430\u0437\u0433\u043E\u0432\u043E\u0440, \u043D\u0435 \u044D\u043A\u0437\u0430\u043C\u0435\u043D!",
        "\u0423 \u043D\u0430\u0441 \u043F\u0430\u043A\u0435\u0442\u044B \u043E\u0442 69.95\u20AC (15 \u043C\u0438\u043D \u0431\u044B\u0441\u0442\u0440\u0430\u044F \u043E\u0446\u0435\u043D\u043A\u0430) \u0434\u043E 249.95\u20AC (40 \u043C\u0438\u043D \u0433\u043B\u0443\u0431\u043E\u043A\u0438\u0439 \u0430\u043D\u0430\u043B\u0438\u0437). \u041A\u0430\u0436\u0434\u044B\u0439 \u043F\u0430\u043A\u0435\u0442 \u0432\u043A\u043B\u044E\u0447\u0430\u0435\u0442 \u043F\u043E\u0434\u0440\u043E\u0431\u043D\u044B\u0439 \u043E\u0442\u0447\u0451\u0442 CEFR.",
        "100% \u043E\u043D\u043B\u0430\u0439\u043D! \u041D\u0443\u0436\u0435\u043D \u0442\u043E\u043B\u044C\u043A\u043E \u043C\u0438\u043A\u0440\u043E\u0444\u043E\u043D \u0438 \u0438\u043D\u0442\u0435\u0440\u043D\u0435\u0442. \u0412\u044B\u0431\u0435\u0440\u0438 \u0443\u0434\u043E\u0431\u043D\u043E\u0435 \u0432\u0440\u0435\u043C\u044F.",
        "\u041E\u0442\u0447\u0451\u0442 \u043F\u0440\u0438\u0434\u0451\u0442 \u0432 \u0442\u0435\u0447\u0435\u043D\u0438\u0435 24 \u0447\u0430\u0441\u043E\u0432. \u0411\u043E\u043B\u044C\u0448\u0438\u043D\u0441\u0442\u0432\u043E \u043F\u043E\u043B\u0443\u0447\u0430\u044E\u0442 \u0435\u0433\u043E \u0437\u0430 \u043D\u0435\u0441\u043A\u043E\u043B\u044C\u043A\u043E \u0447\u0430\u0441\u043E\u0432!"
      ],
      faqCta: "\u0425\u043E\u0447\u0435\u0448\u044C \u043F\u043E\u043F\u0440\u043E\u0431\u043E\u0432\u0430\u0442\u044C?",
      exitEmail: "\u041F\u0440\u0435\u0436\u0434\u0435 \u0447\u0435\u043C \u0443\u0439\u0442\u0438 \u2014 \u0445\u043E\u0447\u0435\u0448\u044C, \u0447\u0442\u043E\u0431\u044B \u041C\u0430\u0440\u043A\u043E \u043E\u0442\u043F\u0440\u0430\u0432\u0438\u043B \u0442\u0435\u0431\u0435 \u0440\u0435\u0437\u044E\u043C\u0435? \u041E\u0441\u0442\u0430\u0432\u044C email \u0438 \u044F \u043D\u0430\u043F\u0438\u0448\u0443 \u0447\u0442\u043E-\u0442\u043E \u043F\u043E\u043B\u0435\u0437\u043D\u043E\u0435.",
      exitSend: "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C",
      exitSkip: "\u041D\u0435\u0442, \u0441\u043F\u0430\u0441\u0438\u0431\u043E",
      emailThanks: "\u041F\u043E\u043B\u0443\u0447\u0438\u043B! \u0421\u043A\u043E\u0440\u043E \u043E\u0442\u043F\u0440\u0430\u0432\u043B\u044E \u0447\u0442\u043E-\u0442\u043E \u043F\u043E\u043B\u0435\u0437\u043D\u043E\u0435. \uD83E\uDD89",
      readyAnytime: "\u042F \u0437\u0434\u0435\u0441\u044C, \u043A\u043E\u0433\u0434\u0430 \u043F\u043E\u043D\u0430\u0434\u043E\u0431\u043B\u044E\u0441\u044C!"
    },
    zh: {
      intentQ: "\u90A3\u4E48\uFF0C\u4F60\u662F\u6765\u68C0\u67E5\u4F60\u7684\u8BED\u8A00\u6C34\u5E73\uFF0C\u8FD8\u662F\u53EA\u662F\u597D\u5947\u6211\u4EEC\u505A\u4EC0\u4E48\uFF1F",
      checkLevel: "\u68C0\u67E5\u6211\u7684\u6C34\u5E73",
      justLooking: "\u53EA\u662F\u770B\u770B",
      whichLang: "\u4F60\u5728\u5B66\u54EA\u79CD\u8BED\u8A00\uFF1F",
      howLong: "\u4F60\u5B66{lang}\u591A\u4E45\u4E86\uFF1F",
      duration: ["\u521A\u5F00\u59CB", "6\u4E2A\u6708-1\u5E74", "1-3\u5E74", "3\u5E74\u4EE5\u4E0A"],
      challengeQ: "\u4F60\u6700\u5927\u7684\u6311\u6218\u662F\u4EC0\u4E48\uFF1F",
      challenges: ["\u53E3\u8BED", "\u8BED\u6CD5", "\u8BCD\u6C47", "\u81EA\u4FE1\u5FC3", "\u5168\u90E8 \uD83D\uDE05"],
      recommend: "\u6839\u636E\u4F60\u544A\u8BC9\u6211\u7684\uFF0C\u6211\u89C9\u5F97{pkg}\u975E\u5E38\u9002\u5408\u4F60\u3002",
      voss: "\u53EA\u7528{time}\u5C31\u80FD\u77E5\u9053\u4F60\u7684\u771F\u5B9E\u6C34\u5E73\uFF0C\u8FD9\u4E0D\u662F\u5F88\u68D2\u5417\uFF1F",
      bookNow: "\u7ACB\u5373\u9884\u7EA6",
      emailOffer: "\u8981\u6211\u628A\u8BE6\u60C5\u53D1\u5230\u4F60\u7684\u90AE\u7BB1\u5417\uFF1F",
      lookingReply: "\u6CA1\u95EE\u9898\uFF01\u6211\u968F\u65F6\u90FD\u5728\u3002\u4EE5\u4E0B\u662F\u5927\u5BB6\u5E38\u95EE\u7684\u95EE\u9898\uFF1A",
      faqBtns: ["\u600E\u4E48\u8FD0\u4F5C\u7684\uFF1F", "\u8D39\u7528\u591A\u5C11\uFF1F", "\u662F\u7EBF\u4E0A\u7684\u5417\uFF1F", "\u591A\u5FEB\u80FD\u62FF\u5230\u7ED3\u679C\uFF1F"],
      faqAnswers: [
        "\u4F60\u9884\u7EA6\u4E00\u4E2A\u65F6\u95F4\uFF0C\u548CMarco\u804A15-40\u5206\u949F\uFF0C\u7136\u540E\u6536\u5230\u5B8C\u6574\u7684CEFR\u62A5\u544A\u548C\u4E2A\u6027\u5316\u4F5C\u4E1A\u3002\u8FD9\u662F\u53CB\u597D\u7684\u804A\u5929\uFF0C\u4E0D\u662F\u53EF\u6015\u7684\u8003\u8BD5\uFF01",
        "\u6211\u4EEC\u670969.95\u20AC\uFF0815\u5206\u949F\u5FEB\u901F\u8BC4\u4F30\uFF09\u5230249.95\u20AC\uFF0840\u5206\u949F\u6DF1\u5EA6\u5206\u6790\uFF09\u7684\u5957\u9910\u3002\u6BCF\u4E2A\u5957\u9910\u90FD\u5305\u542B\u8BE6\u7EC6\u7684CEFR\u62A5\u544A\u3002",
        "100%\u7EBF\u4E0A\uFF01\u4F60\u53EA\u9700\u8981\u9EA6\u514B\u98CE\u548C\u7F51\u7EDC\u8FDE\u63A5\u3002\u9009\u62E9\u4F60\u65B9\u4FBF\u7684\u65F6\u95F4\u3002",
        "24\u5C0F\u65F6\u5185\u6536\u5230\u62A5\u544A\u3002\u5927\u591A\u6570\u4EBA\u51E0\u5C0F\u65F6\u5185\u5C31\u80FD\u6536\u5230\uFF01"
      ],
      faqCta: "\u60F3\u8BD5\u8BD5\u5417\uFF1F",
      exitEmail: "\u5728\u4F60\u79BB\u5F00\u4E4B\u524D\u2014\u2014\u60F3\u8BA9Marco\u7ED9\u4F60\u53D1\u4E2A\u603B\u7ED3\u5417\uFF1F\u7559\u4E0B\u4F60\u7684\u90AE\u7BB1\uFF0C\u6211\u4F1A\u53D1\u4E9B\u6709\u7528\u7684\u4E1C\u897F\u3002",
      exitSend: "\u53D1\u9001",
      exitSkip: "\u4E0D\u7528\u4E86",
      emailThanks: "\u6536\u5230\u4E86\uFF01\u6211\u5F88\u5FEB\u4F1A\u53D1\u7ED9\u4F60\u6709\u7528\u7684\u4FE1\u606F\u3002\uD83E\uDD89",
      readyAnytime: "\u6211\u968F\u65F6\u90FD\u5728\uFF01"
    }
  };

  // ── Package definitions for sales flow ──
  var PACKAGES = [
    { id: 'quick', name: 'Quick Assessment', price: '\u20AC69.95', time: '15 minutes', slug: 'quick' },
    { id: 'full', name: 'Full Assessment', price: '\u20AC129.95', time: '25 minutes', slug: 'full' },
    { id: 'deepdive', name: 'DeepDive Assessment', price: '\u20AC249.95', time: '40 minutes (15 + 25 min)', slug: 'deepdive' }
  ];

  // ── Top 10 learning languages for sales flow ──
  var LEARNING_LANGS = [
    { label: 'English', code: 'en' },
    { label: 'Deutsch', code: 'de' },
    { label: 'Fran\u00E7ais', code: 'fr' },
    { label: 'Espa\u00F1ol', code: 'es' },
    { label: 'Italiano', code: 'it' },
    { label: '\u0420\u0443\u0441\u0441\u043A\u0438\u0439', code: 'ru' },
    { label: '\u4E2D\u6587', code: 'zh' },
    { label: 'Portugu\u00EAs', code: 'pt' },
    { label: 'T\u00FCrk\u00E7e', code: 'tr' },
    { label: '\u65E5\u672C\u8A9E', code: 'ja' }
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
    '#marco-fab{position:fixed;bottom:24px;right:24px;width:50px;height:50px;border-radius:50%;',
    'background:#2563AB;color:#fff;border:none;cursor:pointer;z-index:9999;box-shadow:0 4px 16px rgba(0,0,0,.25);',
    'display:flex;align-items:center;justify-content:center;transition:transform .2s,box-shadow .2s}',
    '#marco-fab img,#marco-fab svg{width:60%;height:60%;object-fit:contain}',
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
    // Sales flow buttons
    '.mc-sales-btns{display:flex;flex-direction:column;gap:6px;margin-top:8px}',
    '.mc-sales-btns button{padding:8px 14px;border-radius:10px;border:1.5px solid #2563AB;background:#fff;color:#2563AB;',
    'font-size:.82rem;font-family:inherit;cursor:pointer;transition:all .15s;text-align:center}',
    '.mc-sales-btns button:hover{background:#2563AB;color:#fff}',
    '.mc-sales-btns button.mc-btn-primary{background:#2563AB;color:#fff}',
    '.mc-sales-btns button.mc-btn-primary:hover{background:#1a4f8a}',
    '.mc-sales-btns button.mc-btn-book{background:#27AE60;color:#fff;border-color:#27AE60;font-weight:600;font-size:.9rem;padding:10px 14px}',
    '.mc-sales-btns button.mc-btn-book:hover{background:#219150}',
    '.mc-sales-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:5px;margin-top:8px}',
    '.mc-sales-grid button{padding:7px 10px;border-radius:8px;border:1px solid #D1D5DB;background:#fff;color:#1C1C1C;',
    'font-size:.8rem;font-family:inherit;cursor:pointer;transition:all .15s;text-align:center}',
    '.mc-sales-grid button:hover{background:#2563AB;color:#fff;border-color:#2563AB}',
    '.mc-pkg-card{background:#F0F7FF;border:1.5px solid #2563AB;border-radius:12px;padding:12px;margin-top:8px}',
    '.mc-pkg-card .mc-pkg-name{font-weight:700;color:#1A3A5C;font-size:.9rem}',
    '.mc-pkg-card .mc-pkg-price{color:#27AE60;font-weight:600;font-size:.85rem;margin-top:2px}',
    '.mc-pkg-card .mc-pkg-voss{font-style:italic;color:#555;font-size:.82rem;margin-top:6px}',
    '@media(max-width:768px){',
    '#marco-fab{width:44px;height:44px;bottom:16px;right:16px}',
    '}',
    '@media(max-width:480px){',
    '#marco-chat{bottom:0;right:0;left:0;width:100%;height:100%;border-radius:0}',
    '#marco-fab{width:40px;height:40px;bottom:16px;right:16px}',
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
  var flowPhase = 'idle'; // idle | lang-confirm | lang-grid | email | sales-intent | sales-lang | sales-duration | sales-challenge | sales-offer | sales-faq | chat
  var salesData = { learningLang: null, learningLangLabel: null, duration: null, challenge: null };
  var exitEmailShown = false;

  // ── Page context detection ──
  var pageContext = (function () {
    var path = window.location.pathname.toLowerCase();
    if (path.indexOf('corporate') !== -1) return 'corporate';
    if (path.indexOf('kids') !== -1) return 'kids';
    if (path.indexOf('partners') !== -1) return 'partners';
    if (path.indexOf('teachers') !== -1) return 'teachers';
    return 'individual';
  })();

  // ── Context-aware greetings and product suggestions ──
  var PAGE_CONTEXT_CONFIG = {
    individual: {
      intentQ: null, // use default SALES_MSGS
      checkLevel: null,
      justLooking: null,
      packages: null // use default PACKAGES
    },
    corporate: {
      intentQ: "Are you looking to assess your team's language skills?",
      checkLevel: "Yes, assess our team",
      justLooking: "Tell me more first",
      packages: [
        { id: 'quick', name: 'Team Quick Assessment', price: '\u20AC69.95', time: '15 min per person', slug: 'quick' },
        { id: 'full', name: 'Team Full Assessment', price: '\u20AC129.95', time: '25 min per person', slug: 'full' },
        { id: 'deepdive', name: 'Team DeepDive Assessment', price: '\u20AC249.95', time: '40 min per person', slug: 'deepdive' }
      ]
    },
    kids: {
      intentQ: "Looking for a fun language session for your child?",
      checkLevel: "Yes, book a session",
      justLooking: "Tell me more first",
      packages: null
    },
    partners: {
      intentQ: "Interested in becoming a LingoGrade partner?",
      checkLevel: "Yes, tell me about partnership",
      justLooking: "Just exploring for now",
      packages: null
    },
    teachers: {
      intentQ: "Want to join our assessor network?",
      checkLevel: "Yes, I'd like to apply",
      justLooking: "Tell me more first",
      packages: null
    }
  };

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

  // ── Helper: get sales messages for current language ──
  function salesMsg() {
    return SALES_MSGS[chosenLang] || SALES_MSGS.en;
  }

  // ── Step 5: Start sales flow (intent question) ──
  function startConversation() {
    showSalesIntent();
  }

  // ── Sales Step 1: Intent question (context-aware) ──
  function showSalesIntent() {
    flowPhase = 'sales-intent';
    setInputEnabled(false);
    var sm = salesMsg();
    var ctx = PAGE_CONTEXT_CONFIG[pageContext] || PAGE_CONTEXT_CONFIG.individual;

    var intentText = ctx.intentQ || sm.intentQ;
    var checkText = ctx.checkLevel || sm.checkLevel;
    var lookText = ctx.justLooking || sm.justLooking;

    var html = intentText +
      '<div class="mc-sales-btns">' +
      '<button class="mc-btn-primary" data-action="check-level">' + checkText + '</button>' +
      '<button data-action="just-looking">' + lookText + '</button>' +
      '</div>';

    var el = addMsgHtml('bot', html);

    el.querySelector('[data-action="check-level"]').addEventListener('click', function () {
      disableButtons(el);
      addMsg('usr', checkText);
      showSalesLangPick();
    });

    el.querySelector('[data-action="just-looking"]').addEventListener('click', function () {
      disableButtons(el);
      addMsg('usr', lookText);
      showFaqFlow();
    });
  }

  // ── Sales Step 2: Which language are you learning? ──
  function showSalesLangPick() {
    flowPhase = 'sales-lang';
    setInputEnabled(false);
    var sm = salesMsg();

    var html = sm.whichLang + '<div class="mc-sales-grid">';
    for (var i = 0; i < LEARNING_LANGS.length; i++) {
      html += '<button data-lang="' + LEARNING_LANGS[i].code + '">' + LEARNING_LANGS[i].label + '</button>';
    }
    html += '</div>';

    var el = addMsgHtml('bot', html);
    var buttons = el.querySelectorAll('.mc-sales-grid button');
    for (var j = 0; j < buttons.length; j++) {
      buttons[j].addEventListener('click', function () {
        var lang = this.getAttribute('data-lang');
        var label = this.textContent;
        salesData.learningLang = lang;
        salesData.learningLangLabel = label;
        disableButtons(el);
        addMsg('usr', label);
        showSalesDuration();
      });
    }
  }

  // ── Sales Step 3: How long have you been learning? ──
  function showSalesDuration() {
    flowPhase = 'sales-duration';
    setInputEnabled(false);
    var sm = salesMsg();
    var question = sm.howLong.replace('{lang}', salesData.learningLangLabel);

    var html = question + '<div class="mc-sales-btns">';
    for (var i = 0; i < sm.duration.length; i++) {
      html += '<button data-idx="' + i + '">' + sm.duration[i] + '</button>';
    }
    html += '</div>';

    var el = addMsgHtml('bot', html);
    var buttons = el.querySelectorAll('.mc-sales-btns button');
    for (var j = 0; j < buttons.length; j++) {
      buttons[j].addEventListener('click', function () {
        var idx = parseInt(this.getAttribute('data-idx'), 10);
        salesData.duration = idx;
        disableButtons(el);
        addMsg('usr', this.textContent);
        showSalesChallenge();
      });
    }
  }

  // ── Sales Step 4: What's your biggest challenge? ──
  function showSalesChallenge() {
    flowPhase = 'sales-challenge';
    setInputEnabled(false);
    var sm = salesMsg();

    var html = sm.challengeQ + '<div class="mc-sales-btns">';
    for (var i = 0; i < sm.challenges.length; i++) {
      html += '<button data-idx="' + i + '">' + sm.challenges[i] + '</button>';
    }
    html += '</div>';

    var el = addMsgHtml('bot', html);
    var buttons = el.querySelectorAll('.mc-sales-btns button');
    for (var j = 0; j < buttons.length; j++) {
      buttons[j].addEventListener('click', function () {
        var idx = parseInt(this.getAttribute('data-idx'), 10);
        salesData.challenge = idx;
        disableButtons(el);
        addMsg('usr', this.textContent);
        showSalesOffer();
      });
    }
  }

  // ── Sales Step 5: Personalized package recommendation ──
  function showSalesOffer() {
    flowPhase = 'sales-offer';
    setInputEnabled(false);
    var sm = salesMsg();

    // Map duration index to package: 0=just started→quick, 1=6mo-1yr→quick, 2=1-3yr→full, 3=3yr+→deepdive
    var ctx = PAGE_CONTEXT_CONFIG[pageContext] || PAGE_CONTEXT_CONFIG.individual;
    var pkgList = ctx.packages || PACKAGES;
    var pkgIdx = salesData.duration;
    if (pkgIdx < 0) pkgIdx = 0;
    if (pkgIdx >= pkgList.length) pkgIdx = pkgList.length - 1;
    var pkg = pkgList[pkgIdx];

    var recText = sm.recommend.replace('{pkg}', pkg.name + ' (' + pkg.price + ')');
    var vossText = sm.voss.replace('{time}', pkg.time);

    var html = '<div class="mc-pkg-card">' +
      '<div class="mc-pkg-name">' + pkg.name + '</div>' +
      '<div class="mc-pkg-price">' + pkg.price + ' \u2014 ' + pkg.time + '</div>' +
      '<div class="mc-pkg-voss">"' + vossText + '"</div>' +
      '</div>' +
      '<div style="margin-top:8px">' + recText + '</div>' +
      '<div class="mc-sales-btns" style="margin-top:10px">' +
      '<a href="https://app.lingograde.com/book?package=' + pkg.slug + '" target="_blank" rel="noopener" ' +
      'style="display:block;text-align:center;padding:10px 14px;border-radius:10px;background:#27AE60;color:#fff;' +
      'font-weight:600;font-size:.9rem;text-decoration:none;transition:background .15s">' + sm.bookNow + '</a>' +
      '</div>';

    var el = addMsgHtml('bot', html);

    // After showing the offer, check if we need email
    setTimeout(function () {
      if (!localStorage.getItem(EMAIL_KEY)) {
        showSalesEmailCapture();
      } else {
        finishSalesFlow();
      }
    }, 800);
  }

  // ── Sales: Email capture after offer (if not yet captured) ──
  function showSalesEmailCapture() {
    var sm = salesMsg();
    var em = EMAIL_MSGS[chosenLang] || EMAIL_MSGS.en;

    var html = sm.emailOffer +
      '<div class="mc-email-block">' +
      '<input type="email" placeholder="' + em.placeholder + '" class="mc-email-input">' +
      '<div class="mc-email-btns">' +
      '<button class="mc-btn-skip" data-action="sales-email-skip">' + (em.skip || 'Skip') + '</button>' +
      '<button class="mc-btn-cont" data-action="sales-email-send">' + (em.cont || 'Send') + '</button>' +
      '</div></div>';

    var el = addMsgHtml('bot', html);
    var emailInput = el.querySelector('.mc-email-input');

    el.querySelector('[data-action="sales-email-skip"]').addEventListener('click', function () {
      disableButtons(el);
      emailInput.disabled = true;
      finishSalesFlow();
    });

    el.querySelector('[data-action="sales-email-send"]').addEventListener('click', function () {
      var email = emailInput.value.trim();
      if (email && email.indexOf('@') !== -1) {
        localStorage.setItem(EMAIL_KEY, email);
        disableButtons(el);
        emailInput.disabled = true;
        addMsg('usr', email);
        var smx = salesMsg();
        addMsg('bot', smx.emailThanks);
        finishSalesFlow();
      } else if (!email) {
        disableButtons(el);
        emailInput.disabled = true;
        finishSalesFlow();
      } else {
        emailInput.style.borderColor = '#EF4444';
        emailInput.focus();
      }
    });

    emailInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        el.querySelector('[data-action="sales-email-send"]').click();
      }
    });
  }

  // ── FAQ flow ("Just looking around") ──
  function showFaqFlow() {
    flowPhase = 'sales-faq';
    setInputEnabled(false);
    var sm = salesMsg();

    var html = sm.lookingReply + '<div class="mc-sales-btns">';
    for (var i = 0; i < sm.faqBtns.length; i++) {
      html += '<button data-idx="' + i + '">' + sm.faqBtns[i] + '</button>';
    }
    html += '</div>';

    var el = addMsgHtml('bot', html);
    var buttons = el.querySelectorAll('.mc-sales-btns button');
    for (var j = 0; j < buttons.length; j++) {
      buttons[j].addEventListener('click', function () {
        var idx = parseInt(this.getAttribute('data-idx'), 10);
        var label = this.textContent;
        disableButtons(el);
        addMsg('usr', label);
        showFaqAnswer(idx);
      });
    }
  }

  // ── FAQ answer + CTA ──
  function showFaqAnswer(idx) {
    var sm = salesMsg();
    var answer = sm.faqAnswers[idx] || sm.faqAnswers[0];

    var html = answer +
      '<div class="mc-sales-btns" style="margin-top:8px">' +
      '<button class="mc-btn-primary" data-action="faq-try">' + sm.faqCta + '</button>' +
      '</div>';

    var el = addMsgHtml('bot', html);

    el.querySelector('[data-action="faq-try"]').addEventListener('click', function () {
      disableButtons(el);
      addMsg('usr', sm.faqCta);
      showSalesLangPick();
    });

    // Also still allow other FAQ buttons to be clicked by showing them again
    setTimeout(function () {
      showFaqMore();
    }, 300);
  }

  // ── Show remaining FAQ buttons or finish ──
  function showFaqMore() {
    var sm = salesMsg();
    var html = '<div class="mc-sales-btns">';
    for (var i = 0; i < sm.faqBtns.length; i++) {
      html += '<button data-idx="' + i + '">' + sm.faqBtns[i] + '</button>';
    }
    html += '</div>';

    var el = addMsgHtml('bot', html);
    var buttons = el.querySelectorAll('.mc-sales-btns button');
    for (var j = 0; j < buttons.length; j++) {
      buttons[j].addEventListener('click', function () {
        var idx = parseInt(this.getAttribute('data-idx'), 10);
        var label = this.textContent;
        disableButtons(el);
        addMsg('usr', label);
        showFaqAnswer(idx);
      });
    }
  }

  // ── Finish sales flow → open general chat ──
  function finishSalesFlow() {
    flowPhase = 'chat';
    setInputEnabled(true);
    var sm = salesMsg();
    addMsg('bot', OWL + ' ' + sm.readyAnytime);
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

  // ── Context-aware greeting text for each page ──
  var PAGE_GREETINGS = {
    individual: null, // use default
    corporate: "Welcome! I can help you find the right language assessment solution for your team.",
    kids: "Hi there! Looking for a fun language session for your child? I can help!",
    partners: "Welcome! Interested in becoming a LingoGrade partner? Let's talk revenue share and referral opportunities.",
    teachers: "Hello! Want to join our assessor network? I can tell you about professional development and earning potential."
  };

  // ── Initial greeting logic ──
  function initGreeting() {
    if (chosenLang) {
      // Language already saved — returning user, go straight to general chat
      flowPhase = 'chat';
      setInputEnabled(true);
      var greeting = GREETINGS[chosenLang] || GREETINGS.en;
      var sm = SALES_MSGS[chosenLang] || SALES_MSGS.en;
      var contextGreeting = PAGE_GREETINGS[pageContext];
      if (contextGreeting) {
        addMsg('bot', OWL + ' ' + contextGreeting);
      } else {
        addMsg('bot', OWL + ' ' + greeting + '\n\n' + sm.readyAnytime);
      }
    } else {
      // No preference yet — show language confirm flow
      showLangConfirm();
    }
  }

  initGreeting();

  // ── Events ──
  fab.addEventListener('click', function () { toggle(true); });
  chat.querySelector('.mc-min').addEventListener('click', function () { toggle(false); });
  chat.querySelector('.mc-close').addEventListener('click', function () {
    if (!localStorage.getItem(EMAIL_KEY) && !exitEmailShown && flowPhase !== 'idle' && flowPhase !== 'lang-confirm' && flowPhase !== 'lang-grid') {
      exitEmailShown = true;
      showExitEmailCapture();
    } else {
      toggle(false);
    }
  });

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  });
  sendBtn.addEventListener('click', send);

  // ── Exit-intent email capture ──
  function showExitEmailCapture() {
    var sm = salesMsg();
    var em = EMAIL_MSGS[chosenLang] || EMAIL_MSGS.en;

    var html = sm.exitEmail +
      '<div class="mc-email-block">' +
      '<input type="email" placeholder="' + em.placeholder + '" class="mc-email-input">' +
      '<div class="mc-email-btns">' +
      '<button class="mc-btn-skip" data-action="exit-skip">' + sm.exitSkip + '</button>' +
      '<button class="mc-btn-cont" data-action="exit-send">' + sm.exitSend + '</button>' +
      '</div></div>';

    var el = addMsgHtml('bot', html);
    var emailInput = el.querySelector('.mc-email-input');

    el.querySelector('[data-action="exit-skip"]').addEventListener('click', function () {
      disableButtons(el);
      emailInput.disabled = true;
      toggle(false);
    });

    el.querySelector('[data-action="exit-send"]').addEventListener('click', function () {
      var email = emailInput.value.trim();
      if (email && email.indexOf('@') !== -1) {
        localStorage.setItem(EMAIL_KEY, email);
        disableButtons(el);
        emailInput.disabled = true;
        addMsg('usr', email);
        addMsg('bot', sm.emailThanks);
        setTimeout(function () { toggle(false); }, 1500);
      } else if (!email) {
        disableButtons(el);
        emailInput.disabled = true;
        toggle(false);
      } else {
        emailInput.style.borderColor = '#EF4444';
        emailInput.focus();
      }
    });

    emailInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        el.querySelector('[data-action="exit-send"]').click();
      }
    });

    msgs.scrollTop = msgs.scrollHeight;
  }

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
