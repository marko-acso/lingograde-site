/**
 * LingoGrade Language Switcher v1.0
 * Lightweight i18n for static HTML pages. No dependencies. <5KB.
 *
 * Usage: Add data-i18n="key" to any element. Include this script.
 * <p data-i18n="hero.title">Default English text</p>
 */
;(function () {
  'use strict';

  var SUPPORTED = ['de','en','fr','es','it','pt','ru','sr','hr','bg','ro','pl'];
  var STORAGE_KEY = 'lg_lang';
  var translations = null;

  function detectLang() {
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved && SUPPORTED.indexOf(saved) !== -1) return saved;
    var nav = (navigator.language || navigator.userLanguage || 'en').split('-')[0].toLowerCase();
    return SUPPORTED.indexOf(nav) !== -1 ? nav : 'en';
  }

  function loadTranslations(cb) {
    if (translations) return cb(translations);
    var base = document.currentScript ? document.currentScript.src.replace(/[^/]*$/, '') : '/i18n/';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', base + 'translations.json', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        try { translations = JSON.parse(xhr.responseText); } catch (e) { translations = {}; }
      } else { translations = {}; }
      cb(translations);
    };
    xhr.onerror = function () { translations = {}; cb(translations); };
    xhr.send();
  }

  function resolve(obj, path) {
    var parts = path.split('.');
    var cur = obj;
    for (var i = 0; i < parts.length; i++) {
      if (!cur || typeof cur !== 'object') return null;
      cur = cur[parts[i]];
    }
    return typeof cur === 'string' ? cur : null;
  }

  function applyLang(lang) {
    loadTranslations(function (t) {
      var langData = t[lang] || t['en'] || {};
      var els = document.querySelectorAll('[data-i18n]');
      for (var i = 0; i < els.length; i++) {
        var key = els[i].getAttribute('data-i18n');
        var val = resolve(langData, key);
        if (val) {
          if (els[i].tagName === 'INPUT' || els[i].tagName === 'TEXTAREA') {
            els[i].placeholder = val;
          } else {
            els[i].textContent = val;
          }
        }
      }
      // Update lang attribute
      document.documentElement.lang = lang;
      // Update active state in switcher
      var btns = document.querySelectorAll('.lg-lang-btn');
      for (var j = 0; j < btns.length; j++) {
        btns[j].classList.toggle('active', btns[j].getAttribute('data-lang') === lang);
      }
      localStorage.setItem(STORAGE_KEY, lang);
    });
  }

  function createSwitcher() {
    var nav = document.querySelector('.nav-menu') || document.querySelector('nav');
    if (!nav) return;

    var wrap = document.createElement('div');
    wrap.className = 'lg-lang-switcher';
    wrap.style.cssText = 'position:relative;display:inline-block;margin-left:8px;';

    var current = detectLang();
    var btn = document.createElement('button');
    btn.className = 'lg-lang-toggle';
    btn.textContent = current.toUpperCase();
    btn.style.cssText = 'background:none;border:1px solid rgba(0,0,0,0.15);border-radius:6px;padding:4px 10px;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;color:inherit;';

    var dropdown = document.createElement('div');
    dropdown.className = 'lg-lang-dropdown';
    dropdown.style.cssText = 'display:none;position:absolute;top:100%;right:0;background:white;border:1px solid #E0E0E0;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1);z-index:999;margin-top:4px;min-width:120px;max-height:300px;overflow-y:auto;';

    var names = {de:'Deutsch',en:'English',fr:'Français',es:'Español',it:'Italiano',pt:'Português',ru:'Русский',sr:'Српски',hr:'Hrvatski',bg:'Български',ro:'Română',pl:'Polski'};

    for (var i = 0; i < SUPPORTED.length; i++) {
      var lang = SUPPORTED[i];
      var item = document.createElement('button');
      item.className = 'lg-lang-btn';
      item.setAttribute('data-lang', lang);
      item.textContent = names[lang] || lang.toUpperCase();
      item.style.cssText = 'display:block;width:100%;text-align:left;padding:8px 16px;border:none;background:none;cursor:pointer;font-size:13px;font-family:inherit;color:#4A4A4A;';
      if (lang === current) item.style.fontWeight = '700';
      item.addEventListener('click', (function (l) {
        return function () {
          applyLang(l);
          btn.textContent = l.toUpperCase();
          dropdown.style.display = 'none';
        };
      })(lang));
      dropdown.appendChild(item);
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
    });
    document.addEventListener('click', function () { dropdown.style.display = 'none'; });

    wrap.appendChild(btn);
    wrap.appendChild(dropdown);
    nav.appendChild(wrap);
  }

  function init() {
    createSwitcher();
    applyLang(detectLang());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
