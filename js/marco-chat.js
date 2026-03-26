/**
 * Marco Chat Widget v1.0 — LingoGrade AI Assistant
 *
 * Floating chat widget powered by Marco the owl.
 * Self-initializing: include <script src="js/marco-chat.js" defer></script>
 *
 * Under 8KB, zero dependencies.
 */
;(function () {
  'use strict';

  var API = 'https://app.lingograde.com/api/chat';
  var STORE_KEY = 'marco_session';
  var MASCOT = 'assets/mascot/marco-hero-tea-mugprint.png';
  var OWL = '\uD83E\uDD89'; // fallback emoji

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

  // ── Greeting ──
  addMsg('bot', "Hey there! I'm Marco \uD83E\uDD89 LingoGrade's friendly owl. Ask me anything about our assessments, pricing, or how it all works!");

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

  function addMsg(type, text) {
    var el = document.createElement('div');
    el.className = 'mc-msg ' + type;
    el.textContent = text;
    msgs.appendChild(el);
    msgs.scrollTop = msgs.scrollHeight;
    return el;
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
      body: JSON.stringify({ message: text, session_id: getSession() })
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
