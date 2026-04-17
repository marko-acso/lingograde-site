/**
 * LingoGrade Cookie Consent — Google Consent Mode v2
 *
 * GA4 loads on every page with consent defaults = "denied", sending
 * anonymized cookieless pings (aggregate page views, no user ID) under
 * legitimate interest. When the user clicks Accept, consent is upgraded
 * to "granted" → full user-level tracking with cookies.
 *
 * Clarity is more invasive (session replay), so it stays gated behind
 * explicit Accept.
 *
 * Consent stored in localStorage key: "lg_cookie_consent"
 * Values: "accepted" | "rejected" | undefined (not yet decided)
 */

(function () {
  'use strict';

  var GA_ID = 'G-32D60T2ZKT';
  var CLARITY_ID = 'w9dq69gmuo';
  var STORAGE_KEY = 'lg_cookie_consent';

  /* ── 0. Consent Mode v2: set defaults BEFORE gtag loads ─────── */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  var storedConsent;
  try { storedConsent = localStorage.getItem(STORAGE_KEY); } catch (e) {}

  /* Default state — denied for everything non-essential.
     If the user already accepted in a prior visit, we still set denied
     first and then call "update" → granted a few lines below. This
     ordering is required by Consent Mode v2. */
  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    personalization_storage: 'denied',
    security_storage: 'granted',
    wait_for_update: 500
  });
  gtag('set', 'ads_data_redaction', true);
  gtag('set', 'url_passthrough', true);

  /* ── 1. Always load GA4 (cookieless pings when denied) ──────── */
  function loadGA() {
    if (document.querySelector('script[src*="googletagmanager"]')) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', GA_ID, { anonymize_ip: true });
  }
  loadGA();

  /* ── 2. If prior visit accepted, upgrade consent now ─────────── */
  function grantConsent() {
    gtag('consent', 'update', {
      ad_storage: 'granted',
      ad_user_data: 'granted',
      ad_personalization: 'granted',
      analytics_storage: 'granted',
      personalization_storage: 'granted'
    });
  }

  /* ── 3. Clarity (session replay) — explicit opt-in only ─────── */
  function loadClarity() {
    if (window.clarity) return;
    (function(c,l,a,r,i,t,y){
      c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", CLARITY_ID);
  }

  if (storedConsent === 'accepted') {
    grantConsent();
    loadClarity();
  }

  /* ── 4. Save consent and act on it ──────────────────────────── */
  function setConsent(value) {
    try { localStorage.setItem(STORAGE_KEY, value); } catch (e) {}
    hideBanner();
    if (value === 'accepted') {
      grantConsent();
      loadClarity();
    }
    /* If rejected: defaults stay denied. GA keeps sending anonymized
       cookieless pings under legitimate interest. */
  }

  /* ── 5. Banner visibility helpers ───────────────────────────── */
  function showBanner() {
    var b = document.getElementById('lg-cookie-banner');
    if (b) b.style.display = 'flex';
  }

  function hideBanner() {
    var b = document.getElementById('lg-cookie-banner');
    if (b) {
      b.style.opacity = '0';
      b.style.transform = 'translateY(16px)';
      setTimeout(function () { b.style.display = 'none'; }, 300);
    }
  }

  /* ── 6. Inject banner HTML + CSS ────────────────────────────── */
  function injectBanner() {
    if (document.getElementById('lg-cookie-banner')) return;

    var style = document.createElement('style');
    style.textContent = [
      '#lg-cookie-banner {',
      '  position: fixed;',
      '  bottom: 0;',
      '  left: 0;',
      '  right: 0;',
      '  z-index: 99999;',
      '  display: flex;',
      '  align-items: center;',
      '  justify-content: space-between;',
      '  flex-wrap: wrap;',
      '  gap: 12px;',
      '  padding: 14px 24px;',
      '  background: #1A2E52;',
      '  color: #F0F6FF;',
      '  font-family: "DM Sans", -apple-system, sans-serif;',
      '  font-size: 0.875rem;',
      '  line-height: 1.5;',
      '  border-top: 3px solid #27AE60;',
      '  box-shadow: 0 -4px 24px rgba(0,0,0,0.18);',
      '  opacity: 1;',
      '  transform: translateY(0);',
      '  transition: opacity 0.3s ease, transform 0.3s ease;',
      '}',
      '#lg-cookie-banner p {',
      '  margin: 0;',
      '  flex: 1 1 280px;',
      '}',
      '#lg-cookie-banner a {',
      '  color: #60A5FA;',
      '  text-decoration: underline;',
      '  text-underline-offset: 2px;',
      '}',
      '#lg-cookie-banner a:hover {',
      '  color: #93C5FD;',
      '}',
      '.lg-cookie-actions {',
      '  display: flex;',
      '  gap: 10px;',
      '  flex-shrink: 0;',
      '  flex-wrap: wrap;',
      '}',
      '.lg-btn-accept {',
      '  padding: 9px 22px;',
      '  background: #27AE60;',
      '  color: #fff;',
      '  border: none;',
      '  border-radius: 8px;',
      '  font-family: inherit;',
      '  font-size: 0.875rem;',
      '  font-weight: 600;',
      '  cursor: pointer;',
      '  transition: background 0.15s;',
      '}',
      '.lg-btn-accept:hover { background: #219150; }',
      '.lg-btn-reject {',
      '  padding: 9px 22px;',
      '  background: transparent;',
      '  color: #CBD5E1;',
      '  border: 1.5px solid #4B6A9A;',
      '  border-radius: 8px;',
      '  font-family: inherit;',
      '  font-size: 0.875rem;',
      '  font-weight: 500;',
      '  cursor: pointer;',
      '  transition: border-color 0.15s, color 0.15s;',
      '}',
      '.lg-btn-reject:hover { border-color: #7A9AC8; color: #E2E8F0; }',
      '@media (max-width: 600px) {',
      '  #lg-cookie-banner { padding: 14px 16px; }',
      '  .lg-cookie-actions { width: 100%; }',
      '  .lg-btn-accept, .lg-btn-reject { flex: 1; text-align: center; }',
      '}'
    ].join('\n');
    document.head.appendChild(style);

    var banner = document.createElement('div');
    banner.id = 'lg-cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.innerHTML = [
      '<p>',
      '  We collect anonymous usage stats to improve the site. ',
      '  Click <strong>Accept</strong> to also allow personalised analytics ',
      '  (Google Analytics cookies + Microsoft Clarity session replay). ',
      '  Read our <a href="/privacy-policy.html">Privacy Policy</a>.',
      '</p>',
      '<div class="lg-cookie-actions">',
      '  <button class="lg-btn-reject" id="lg-cookie-reject" aria-label="Reject non-essential cookies">Reject</button>',
      '  <button class="lg-btn-accept" id="lg-cookie-accept" aria-label="Accept cookies">Accept</button>',
      '</div>'
    ].join('');

    document.body.appendChild(banner);

    document.getElementById('lg-cookie-accept').addEventListener('click', function () {
      setConsent('accepted');
    });
    document.getElementById('lg-cookie-reject').addEventListener('click', function () {
      setConsent('rejected');
    });
  }

  /* ── 7. Boot ──────────────────────────────────────────────────── */
  if (!storedConsent) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', injectBanner);
    } else {
      injectBanner();
    }
  }
})();
