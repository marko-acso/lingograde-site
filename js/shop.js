// Lightbox for sticker images
function enlargeImage(src) {
  var overlay = document.createElement('div');
  overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;cursor:pointer;';
  var img = document.createElement('img');
  img.src = src;
  img.style.cssText = 'max-width:90%;max-height:90%;border-radius:12px;box-shadow:0 0 40px rgba(0,0,0,0.5);';
  overlay.appendChild(img);
  overlay.onclick = function() { document.body.removeChild(overlay); };
  document.body.appendChild(overlay);
}

// Marco gallery popup
(function() {
  var marcoSrcs = ['assets/mascot/Marco4.webp', 'assets/mascot/Marco.webp', 'assets/mascot/Marco2.webp'];
  var currentIdx = 0;

  document.querySelectorAll('[data-marco-gallery]').forEach(function(img, i) {
    img.addEventListener('click', function() {
      currentIdx = i;
      openMarcoGallery();
    });
  });

  function openMarcoGallery() {
    var overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);display:flex;align-items:center;justify-content:center;z-index:10000;';

    var container = document.createElement('div');
    container.style.cssText = 'position:relative;display:flex;align-items:center;gap:16px;max-width:95%;';

    var btnStyle = 'background:rgba(255,255,255,0.15);border:none;color:#fff;font-size:2rem;width:48px;height:48px;border-radius:50%;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;';

    var prevBtn = document.createElement('button');
    prevBtn.innerHTML = '&#8249;';
    prevBtn.style.cssText = btnStyle;
    prevBtn.onclick = function(e) { e.stopPropagation(); currentIdx = (currentIdx - 1 + marcoSrcs.length) % marcoSrcs.length; mainImg.src = marcoSrcs[currentIdx]; updateThumbs(); };

    var mainImg = document.createElement('img');
    mainImg.src = marcoSrcs[currentIdx];
    mainImg.style.cssText = 'max-width:min(500px,75vw);max-height:80vh;border-radius:12px;box-shadow:0 0 40px rgba(0,0,0,0.5);';

    var nextBtn = document.createElement('button');
    nextBtn.innerHTML = '&#8250;';
    nextBtn.style.cssText = btnStyle;
    nextBtn.onclick = function(e) { e.stopPropagation(); currentIdx = (currentIdx + 1) % marcoSrcs.length; mainImg.src = marcoSrcs[currentIdx]; updateThumbs(); };

    container.appendChild(prevBtn);
    container.appendChild(mainImg);
    container.appendChild(nextBtn);

    var thumbRow = document.createElement('div');
    thumbRow.style.cssText = 'position:absolute;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:10px;';

    var thumbs = [];
    marcoSrcs.forEach(function(src, i) {
      var t = document.createElement('img');
      t.src = src;
      t.style.cssText = 'width:60px;height:60px;object-fit:cover;border-radius:8px;cursor:pointer;border:2px solid ' + (i === currentIdx ? '#27AE60' : 'transparent') + ';opacity:' + (i === currentIdx ? '1' : '0.6') + ';transition:all 0.2s;';
      t.onclick = function(e) { e.stopPropagation(); currentIdx = i; mainImg.src = marcoSrcs[i]; updateThumbs(); };
      thumbRow.appendChild(t);
      thumbs.push(t);
    });

    function updateThumbs() {
      thumbs.forEach(function(t, i) {
        t.style.borderColor = i === currentIdx ? '#27AE60' : 'transparent';
        t.style.opacity = i === currentIdx ? '1' : '0.6';
      });
    }

    var closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.style.cssText = 'position:absolute;top:16px;right:20px;background:none;border:none;color:#fff;font-size:2.5rem;cursor:pointer;z-index:10001;';
    closeBtn.onclick = function() { document.body.removeChild(overlay); };

    overlay.appendChild(container);
    overlay.appendChild(thumbRow);
    overlay.appendChild(closeBtn);
    overlay.onclick = function(e) { if (e.target === overlay) document.body.removeChild(overlay); };
    document.body.appendChild(overlay);

    document.addEventListener('keydown', function handler(e) {
      if (e.key === 'Escape') { if (overlay.parentNode) document.body.removeChild(overlay); document.removeEventListener('keydown', handler); }
      if (e.key === 'ArrowLeft') { prevBtn.click(); }
      if (e.key === 'ArrowRight') { nextBtn.click(); }
    });
  }
})();

// Currency geo-detection — IP geolocation with timezone fallback
(function(){
  var COUNTRY_CURRENCY = {US:'USD',GB:'GBP',CH:'CHF',LI:'CHF',CN:'CNY',HK:'CNY',MO:'CNY'};
  var SYMBOLS = {EUR:'\u20AC',USD:'$',GBP:'\u00A3',CHF:'CHF\u00A0',CNY:'\u00A5'};

  var eurToUsd = {
    '5.00':'5.00','10.00':'10.00','20.00':'20.00','12.95':'12.95','14.95':'14.95',
    '19.95':'22.95','24.95':'29.95','29.95':'29.95','37.95':'43.95','44.90':'52.90',
    '44.95':'51.95','59.95':'68.85','84.80':'99.80','129.95':'129.95','139.95':'139.95',
    '299.95':'349.95','384.75':'449.70'
  };
  var eurToCny = {
    '5.00':'8','10.00':'18','20.00':'88','12.95':'99.95','14.95':'99.95',
    '19.95':'149.95','24.95':'199.95','29.95':'249.95','37.95':'299.95','44.90':'349.95',
    '44.95':'349.95','59.95':'449.95','84.80':'649.95','129.95':'999.95','139.95':'999.95',
    '299.95':'2288.95','384.75':'2899.95'
  };
  var PRICE_MAPS = {USD:eurToUsd,CNY:eurToCny};
  window._lgEurToUsd = eurToUsd;

  function tzFallback() {
    var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    if (/America\/(New_York|Chicago|Denver|Los_Angeles|Anchorage|Phoenix|Detroit|Indiana|Kentucky|Boise|Juneau|Sitka|Yakutat|Nome|Adak|Menominee|North_Dakota)|Pacific\/Honolulu|US\//.test(tz)) return 'USD';
    if (/Europe\/London|Europe\/Belfast|Europe\/Isle_of_Man|Europe\/Jersey|Europe\/Guernsey/.test(tz)) return 'GBP';
    if (/Europe\/Zurich/.test(tz)) return 'CHF';
    if (/Asia\/(Shanghai|Chongqing|Harbin|Urumqi|Hong_Kong|Macau)/.test(tz)) return 'CNY';
    return 'EUR';
  }

  // Save originals once so we can re-apply on geo override
  var origDataPrices = [];
  var origTextNodes = [];
  var origAttrs = [];
  var origTierLabels = [];
  var saved = false;

  function saveOriginals() {
    if (saved) return;
    document.querySelectorAll('[data-price]').forEach(function(el){
      origDataPrices.push({el:el, eur:el.getAttribute('data-price'), text:el.textContent});
    });
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    var n;
    while (n = walker.nextNode()) {
      if (n.nodeValue.indexOf('EUR') !== -1) origTextNodes.push({node:n, text:n.nodeValue});
    }
    document.querySelectorAll('[data-tip],[data-title]').forEach(function(el){
      ['data-tip','data-title'].forEach(function(attr){
        var v = el.getAttribute(attr);
        if (v && v.indexOf('EUR') !== -1) origAttrs.push({el:el, attr:attr, val:v});
      });
    });
    document.querySelectorAll('.sticker-tier-option').forEach(function(el){
      origTierLabels.push({el:el, html:el.innerHTML});
    });
    saved = true;
  }

  var currentCode = null;

  function applyPrices(code) {
    if (code === currentCode) return;
    currentCode = code;
    var symbol = SYMBOLS[code] || SYMBOLS.EUR;
    var isUSD = code === 'USD';
    var isCNY = code === 'CNY';
    var priceMap = PRICE_MAPS[code] || null;

    window._lgCurrency = symbol;
    window._lgIsUSD = isUSD;
    window._lgIsCNY = isCNY;
    window._lgConvertPrice = function(eurPrice) {
      return priceMap ? (priceMap[eurPrice] || eurPrice) : eurPrice;
    };

    // data-price elements
    origDataPrices.forEach(function(o){
      var converted = priceMap ? (priceMap[o.eur] || o.eur) : o.eur;
      o.el.textContent = symbol + converted;
      o.el.setAttribute('data-price', isUSD ? converted : o.eur);
    });

    // Text nodes — always restore from EUR originals then convert
    origTextNodes.forEach(function(o){
      if (code === 'EUR') { o.node.nodeValue = o.text; return; }
      o.node.nodeValue = o.text.replace(/EUR\s?([\d,]+\.?\d*)/g, function(m, p){
        var clean = p.replace(/,/g, '');
        return symbol + (priceMap ? (priceMap[clean] || clean) : clean);
      });
    });

    // data-tip / data-title attributes
    origAttrs.forEach(function(o){
      if (code === 'EUR') { o.el.setAttribute(o.attr, o.val); return; }
      o.el.setAttribute(o.attr, o.val.replace(/EUR\s?([\d,]+\.?\d*)/g, function(m, p){
        var clean = p.replace(/,/g, '');
        return symbol + (priceMap ? (priceMap[clean] || clean) : clean);
      }));
    });

    // Sticker tier labels — restore then convert
    origTierLabels.forEach(function(o){
      o.el.innerHTML = o.html; // restore EUR originals
      if (isUSD) {
        Object.keys(eurToUsd).forEach(function(eur){
          o.el.innerHTML = o.el.innerHTML.replace(new RegExp('\u20AC' + eur.replace('.', '\\.'), 'g'), '$' + eurToUsd[eur]);
        });
        o.el.innerHTML = o.el.innerHTML.replace(/\u20AC18\.95\/pack/g, '$21.95/pack');
        o.el.innerHTML = o.el.innerHTML.replace(/\u20AC14\.95\/pack/g, '$17.33/pack');
        o.el.innerHTML = o.el.innerHTML.replace(/\u20AC1\.95/g, '$1.95');
        o.el.innerHTML = o.el.innerHTML.replace(/\u20AC14\.95/g, '$17.95');
      }
    });

    // CNY bundle toggle
    var cnBundle = document.getElementById('cn-bundle');
    if (cnBundle) cnBundle.style.display = isCNY ? '' : 'none';

    // Re-run sticker total
    if (typeof updateStickerTotal === 'function') updateStickerTotal();
  }

  saveOriginals();
  applyPrices(tzFallback()); // instant render with timezone guess

  // Override with geo-IP if different
  fetch('https://api.country.is/')
    .then(function(r){ return r.json(); })
    .then(function(d){
      var cc = d && d.country;
      if (cc && COUNTRY_CURRENCY[cc]) applyPrices(COUNTRY_CURRENCY[cc]);
    })
    .catch(function(){}); // silently keep timezone result
})();

// Sticker order total
function updateStickerTotal(){
  var tierPricesEUR = { '1': 19.95, '2': 37.95, '3': 44.95 };
  var tierPricesUSD = { '1': 22.95, '2': 43.95, '3': 51.95 };
  var tierPrices = window._lgIsUSD ? tierPricesUSD : tierPricesEUR;
  var tierEl = document.querySelector('input[name="sticker-tier"]:checked');
  var tier = tierEl ? tierEl.value : '3';
  var defaultPrice = window._lgIsUSD ? 51.95 : 44.95;
  var total = (tierPrices[tier] || defaultPrice).toFixed(2);
  var el = document.getElementById('sticker-total');
  el.textContent = (window._lgCurrency || '\u20AC') + total;

  document.querySelectorAll('.sticker-tier-option').forEach(function(opt){
    var isSel = opt.getAttribute('data-tier') === tier;
    if(opt.getAttribute('data-tier') === '3'){
      opt.style.borderColor = isSel ? 'var(--accent)' : 'var(--border)';
      opt.style.boxShadow = isSel ? '0 0 0 1px var(--accent)' : 'none';
      opt.style.background = isSel ? 'linear-gradient(135deg,rgba(37,99,171,0.15),rgba(37,99,171,0.08))' : '#1e1e1e';
    } else {
      opt.style.borderColor = isSel ? 'var(--accent)' : 'var(--border)';
      opt.style.boxShadow = isSel ? '0 0 0 1px var(--accent)' : 'none';
    }
  });
}
updateStickerTotal();

// Sync dropdown with carousel
var stickerSelect = document.getElementById('sticker-set');
var packOrder = ['marco','mila','corporate','playful','kids'];

var packData = {
  marco: {
    desc: '30 Marco stickers in 3 designs + 5 bonus LingoGrade standard',
    imgs: ['assets/mascot/lingograde-card.webp','assets/mascot/marco-face-wink.webp','assets/mascot/marco-hero.webp?v=3','assets/mascot/marco-logo-v6.1.webp?v=3']
  },
  mila: {
    desc: '30 Mila stickers in 3 designs + 5 bonus LingoGrade standard',
    imgs: ['assets/mascot/lingograde-card-mila.webp','assets/mascot/marco-face-party.webp','assets/mascot/mila-hero.webp?v=1','assets/mascot/marco-logo-v6.1.webp?v=3']
  },
  corporate: {
    desc: '30 Corporate stickers in 3 designs (Marco + Mila in uniform) + 5 bonus LingoGrade standard',
    imgs: ['assets/mascot/lingograde-card-corporate.webp','assets/mascot/lingograde-card.webp','assets/mascot/lingograde-card-mila.webp','assets/mascot/marco-logo-v6.1.webp?v=3']
  },
  playful: {
    desc: '30 Playful stickers in 3 designs (Marco + Mila casual) + 5 bonus LingoGrade standard',
    imgs: ['assets/mascot/lingograde-card-kids.webp','assets/mascot/lingograde-card.webp','assets/mascot/lingograde-card-mila.webp','assets/mascot/marco-logo-v6.1.webp?v=3']
  },
  kids: {
    desc: '30 Kids stickers in 3 designs + 5 bonus LingoGrade standard',
    imgs: ['assets/mascot/marco-wave.webp','assets/mascot/lingograde-card-kids.webp','assets/mascot/marco-face-wink.webp','assets/mascot/marco-logo-v6.1.webp?v=3']
  }
};

function selectPack(pack){
  // Update preview panel
  var preview = document.getElementById('pack-preview');
  var desc = document.getElementById('pack-preview-desc');
  var thumbs = document.getElementById('pack-preview-thumbs');
  if (preview && desc && packData[pack]) {
    preview.classList.add('visible');
    desc.textContent = packData[pack].desc;
    var imgs = thumbs.querySelectorAll('.preview-thumb');
    packData[pack].imgs.forEach(function(src, i){
      if (imgs[i]) imgs[i].src = src;
    });
  }
  // Sync dropdown
  if (stickerSelect.value !== pack) stickerSelect.value = pack;
}

// 3D Carousel Navigation
var currentSlide = 1; // Start with Mila (index 1) active
var carouselItems = document.querySelectorAll('.carousel-item');
var campaignNames = ['Marco - Marco solo', 'Mila - Mila solo', 'Corporate - Marco + Mila in uniform', 'Playful - Marco + Mila casual', 'Kids - fun and playful'];

function updateCarousel() {
  var items = document.querySelectorAll('.carousel-item');
  var total = items.length;
  items.forEach(function(item) {
    item.className = 'carousel-item';
    var idx = parseInt(item.dataset.index);
    var diff = idx - currentSlide;
    // Wrap around
    if (diff > 2) diff -= total;
    if (diff < -2) diff += total;

    if (diff === 0) item.classList.add('active');
    else if (diff === -1) item.classList.add('prev');
    else if (diff === 1) item.classList.add('next');
    else if (diff === -2 || diff <= -2) item.classList.add('far-prev');
    else item.classList.add('far-next');

    // Re-add campaign
    item.setAttribute('data-campaign', item.getAttribute('data-campaign'));
  });
  document.getElementById('carousel-label').textContent = campaignNames[currentSlide];
  // Sync dropdown
  var dd = document.getElementById('sticker-set');
  if (dd) dd.selectedIndex = currentSlide;
  // Sync pack selection
  selectPack(packOrder[currentSlide]);
  updateStickerTotal();
  // Sync SKU preview with active campaign + frame color
  if (typeof updateSkuPreview === 'function') updateSkuPreview();
}

function goToSlide(idx) { currentSlide = idx; updateCarousel(); }
function nextSlide() { currentSlide = (currentSlide + 1) % 5; updateCarousel(); }
function prevSlide() { currentSlide = (currentSlide - 1 + 5) % 5; updateCarousel(); }

// Dropdown changes drive carousel
stickerSelect.addEventListener('change', function(){
  var idx = packOrder.indexOf(stickerSelect.value);
  if (idx >= 0) goToSlide(idx);
});

// Touch swipe on carousel
(function() {
  var el = document.querySelector('.carousel-wrapper');
  if (!el) return;
  var startX;
  el.addEventListener('touchstart', function(e) { startX = e.touches[0].clientX; });
  el.addEventListener('touchend', function(e) {
    var diff = e.changedTouches[0].clientX - startX;
    if (Math.abs(diff) > 40) { diff > 0 ? prevSlide() : nextSlide(); }
  });
})();

// Referral param forwarding
(function(){
  var ref = new URLSearchParams(window.location.search).get('ref');
  if (!ref) return;
  document.querySelectorAll('a[href*="app.lingograde.com"]').forEach(function(a){
    var url = new URL(a.href);
    url.searchParams.set('ref', ref.toUpperCase());
    a.href = url.toString();
  });
})();

// ── Step card mobile bottom-sheet modal ──
(function(){
  var overlay = document.getElementById('stepModalOverlay');
  var modal   = document.getElementById('stepModal');
  var mTitle  = document.getElementById('stepModalTitle');
  var mBody   = document.getElementById('stepModalBody');
  if (!overlay || !modal) return;

  function openModal(title, body) {
    mTitle.textContent = title;
    mBody.innerHTML = body;
    overlay.classList.add('active');
    modal.classList.add('active');
  }
  function closeModal() {
    modal.classList.remove('active');
    overlay.classList.remove('active');
  }

  // Only attach tap handlers on mobile (<= 768px)
  function isMobile() { return window.matchMedia('(max-width: 768px)').matches; }

  document.querySelectorAll('.guide-step[data-tip]').forEach(function(step) {
    step.addEventListener('click', function() {
      if (!isMobile()) return;
      openModal(step.getAttribute('data-title'), step.getAttribute('data-tip'));
    });
  });

  overlay.addEventListener('click', closeModal);

  // Swipe-down to close
  var startY = 0;
  modal.addEventListener('touchstart', function(e) { startY = e.touches[0].clientY; }, { passive: true });
  modal.addEventListener('touchmove', function(e) {
    var dy = e.touches[0].clientY - startY;
    if (dy > 60) closeModal();
  }, { passive: true });
})();

// ── Frame Color Picker + SKU Preview ──
var currentFrame = 'blue';
var frameColors = { blue: '#2563AB', gold: '#C5960C', grey: '#3A3A3A' };

// Map carousel campaign names → SKU filename prefixes (from generate_framed_skus.py)
var campaignToSku = {
  marco: 'marco_hero',
  mila: 'mila_wave',
  corporate: 'corporate_duo',
  playful: 'playful_duo',
  kids: 'kids_marco_abc'
};

function getActiveCampaign() {
  var active = document.querySelector('.carousel-item.active');
  return active ? active.getAttribute('data-campaign') : 'mila';
}

function updateSkuPreview() {
  var img = document.getElementById('sku-preview-img');
  if (!img) return;
  var campaign = getActiveCampaign();
  var sku = campaignToSku[campaign] || 'mila_wave';
  var src = 'assets/stickers/framed_web/sku_' + sku + '_' + currentFrame + '.png';
  img.style.opacity = '0';
  setTimeout(function() {
    img.src = src;
    img.alt = campaign + ' sticker - ' + currentFrame + ' frame';
    img.style.opacity = '1';
  }, 150);
}

function selectFrame(color) {
  currentFrame = color;
  // Update swatch active state
  document.querySelectorAll('.frame-swatch').forEach(function(s) {
    s.classList.toggle('active', s.getAttribute('data-frame') === color);
  });
  // Update carousel item borders to reflect frame color
  document.querySelectorAll('.carousel-item').forEach(function(item) {
    item.classList.remove('frame-blue', 'frame-gold', 'frame-grey');
    item.classList.add('frame-' + color);
  });
  // Update bracket overlay stroke colors to match frame
  var hex = frameColors[color];
  document.querySelectorAll('.carousel-item .bracket-overlay path').forEach(function(path) {
    path.setAttribute('stroke', hex);
  });
  document.querySelectorAll('.carousel-item .scan-me-label').forEach(function(label) {
    label.style.color = hex;
  });
  // Update SKU preview image
  updateSkuPreview();
}
// Initialize frame on load
selectFrame('blue');

// ── Sticker Map (Leaflet + API-backed with fallback) ──
document.addEventListener('DOMContentLoaded', function() {
  var mapEl = document.getElementById('sticker-map-container');
  if (!mapEl || typeof L === 'undefined') return;
  mapEl.id = 'sticker-map-leaf';
  mapEl.style.height = '420px';
  mapEl.style.width = '100%';
  mapEl.style.borderRadius = '16px';

  var map = L.map('sticker-map-leaf', {
    center: [35, 15],
    zoom: 3,
    minZoom: 2,
    maxZoom: 12,
    scrollWheelZoom: false,
    attributionControl: true
  });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(map);

  // Fallback data — used when API is unreachable or returns empty
  var fallbackPlacements = [
    { lat: 42.6977, lng: 23.3219, city: 'Sofia', count: 18 },
    { lat: 48.2082, lng: 16.3738, city: 'Vienna', count: 12 },
    { lat: 52.5200, lng: 13.4050, city: 'Berlin', count: 9 },
    { lat: 48.8566, lng: 2.3522, city: 'Paris', count: 7 },
    { lat: 51.5074, lng: -0.1278, city: 'London', count: 8 },
    { lat: 47.3769, lng: 8.5417, city: 'Zurich', count: 11 },
    { lat: 41.9028, lng: 12.4964, city: 'Rome', count: 5 },
    { lat: 40.4168, lng: -3.7038, city: 'Madrid', count: 4 },
    { lat: 55.6761, lng: 12.5683, city: 'Copenhagen', count: 3 },
    { lat: 59.3293, lng: 18.0686, city: 'Stockholm', count: 3 },
    { lat: 50.0755, lng: 14.4378, city: 'Prague', count: 6 },
    { lat: 47.4979, lng: 19.0402, city: 'Budapest', count: 4 },
    { lat: 44.4268, lng: 26.1025, city: 'Bucharest', count: 3 },
    { lat: 40.7128, lng: -74.0060, city: 'New York', count: 5 },
    { lat: 37.7749, lng: -122.4194, city: 'San Francisco', count: 3 },
    { lat: 43.7696, lng: 11.2558, city: 'Florence', count: 2 },
    { lat: 45.4642, lng: 9.1900, city: 'Milan', count: 4 },
    { lat: 52.3676, lng: 4.9041, city: 'Amsterdam', count: 5 },
    { lat: 38.7223, lng: -9.1393, city: 'Lisbon', count: 3 },
    { lat: 53.3498, lng: -6.2603, city: 'Dublin', count: 2 },
    { lat: 46.2044, lng: 6.1432, city: 'Geneva', count: 3 },
    { lat: 42.3601, lng: -71.0589, city: 'Boston', count: 2 },
    { lat: 41.0082, lng: 28.9784, city: 'Istanbul', count: 3 },
    { lat: 35.6762, lng: 139.6503, city: 'Tokyo', count: 2 },
    { lat: 22.3193, lng: 114.1694, city: 'Hong Kong', count: 2 },
    { lat: -33.8688, lng: 151.2093, city: 'Sydney', count: 1 },
    { lat: 25.2048, lng: 55.2708, city: 'Dubai', count: 2 },
    { lat: 1.3521, lng: 103.8198, city: 'Singapore', count: 1 }
  ];
  var fallbackStats = { total: 127, countries: 14, cities: 38 };

  function renderMarkers(placements) {
    placements.forEach(function(p) {
      var size = Math.min(12, 6 + p.count * 0.5);
      var partnerLine = p.partner ? '<br><span class="fs-smm" style="color:#888;" >' + p.partner + '</span>' : '';
      L.circleMarker([p.lat, p.lng], {
        radius: size,
        fillColor: '#2563AB',
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.85
      }).addTo(map).bindPopup(
        '<div class="text-center" style="font-family:DM Sans,sans-serif;">' +
        '<strong class="fs-base" >' + p.city + '</strong><br>' +
        '<span class="fw-700 c-accent" >' + p.count + '</span> sticker' + (p.count > 1 ? 's' : '') + ' placed' +
        partnerLine +
        '</div>'
      );
    });
  }

  function updateStats(stats) {
    var el;
    el = document.getElementById('map-total-stickers'); if (el) el.textContent = stats.total;
    el = document.getElementById('map-total-countries'); if (el) el.textContent = stats.countries;
    el = document.getElementById('map-total-cities'); if (el) el.textContent = stats.cities;
  }

  // Try API first, fall back to hardcoded sample data
  var API = window.LG_API || 'https://api.lingograde.com';
  fetch(API + '/v1/stickers/map')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.placements && data.placements.length > 0) {
        renderMarkers(data.placements);
        updateStats(data.stats);
        var badge = document.getElementById('map-preview-badge');
        if (badge) badge.style.display = 'none';
      } else {
        renderMarkers(fallbackPlacements);
        updateStats(fallbackStats);
      }
    })
    .catch(function() {
      renderMarkers(fallbackPlacements);
      updateStats(fallbackStats);
    });

  // Responsive height
  function resizeMap() {
    var h = window.innerWidth <= 768 ? 280 : 420;
    mapEl.style.height = h + 'px';
    map.invalidateSize();
  }
  window.addEventListener('resize', resizeMap);
});

// ── Hover Zoom Lens (Amazon-style magnifier) ──
(function() {
  var ZOOM = 2.5;
  var LENS_SIZE = 180;
  var isMobile = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  if (isMobile) return; // Mobile uses tap-to-lightbox instead

  document.querySelectorAll('[data-zoom]').forEach(function(img) {
    var lens = null;
    var result = null;

    img.addEventListener('mouseenter', function() {
      // Create lens overlay
      lens = document.createElement('div');
      lens.style.cssText = 'position:absolute;width:' + LENS_SIZE + 'px;height:' + LENS_SIZE + 'px;border:2px solid var(--accent);border-radius:50%;pointer-events:none;z-index:100;box-shadow:0 0 0 1px rgba(0,0,0,0.3),0 4px 16px rgba(0,0,0,0.3);background-repeat:no-repeat;cursor:none;';

      // Create magnified preview panel
      result = document.createElement('div');
      result.style.cssText = 'position:absolute;top:0;left:calc(100% + 16px);width:320px;height:320px;border:1px solid var(--border);border-radius:12px;background-repeat:no-repeat;z-index:100;box-shadow:0 8px 32px rgba(0,0,0,0.4);background-color:#1e1e1e;';

      // Make parent relative
      var parent = img.parentElement;
      if (getComputedStyle(parent).position === 'static') {
        parent.style.position = 'relative';
      }
      parent.appendChild(lens);
      parent.appendChild(result);

      // Set background images
      lens.style.backgroundImage = 'url(' + img.src + ')';
      result.style.backgroundImage = 'url(' + img.src + ')';
    });

    img.addEventListener('mousemove', function(e) {
      if (!lens || !result) return;
      var rect = img.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;

      // Clamp
      x = Math.max(0, Math.min(x, rect.width));
      y = Math.max(0, Math.min(y, rect.height));

      // Percentages
      var pctX = x / rect.width;
      var pctY = y / rect.height;

      // Position lens centered on cursor
      var parentRect = img.parentElement.getBoundingClientRect();
      var lensX = (rect.left - parentRect.left) + x - LENS_SIZE / 2;
      var lensY = (rect.top - parentRect.top) + y - LENS_SIZE / 2;
      lens.style.left = lensX + 'px';
      lens.style.top = lensY + 'px';

      // Lens background (zoomed portion under lens)
      var lensZoom = ZOOM;
      lens.style.backgroundSize = (rect.width * lensZoom) + 'px ' + (rect.height * lensZoom) + 'px';
      lens.style.backgroundPosition = -(x * lensZoom - LENS_SIZE / 2) + 'px ' + -(y * lensZoom - LENS_SIZE / 2) + 'px';

      // Result panel background
      result.style.backgroundSize = (rect.width * ZOOM * 1.8) + 'px ' + (rect.height * ZOOM * 1.8) + 'px';
      result.style.backgroundPosition = -(pctX * rect.width * ZOOM * 1.8 - 160) + 'px ' + -(pctY * rect.height * ZOOM * 1.8 - 160) + 'px';
    });

    img.addEventListener('mouseleave', function() {
      if (lens && lens.parentNode) lens.parentNode.removeChild(lens);
      if (result && result.parentNode) result.parentNode.removeChild(result);
      lens = null;
      result = null;
    });
  });
})();

// ── Waitlist signup ──
// TODO: When a backend endpoint is ready, replace the localStorage fallback below
// with a real POST to https://app.lingograde.com/api/waitlist (or equivalent).
function joinWaitlist(btn, product) {
  var form = btn.closest('.waitlist-form');
  var input = form.querySelector('input[type="email"]');
  var email = input ? input.value.trim() : '';

  // Basic email validation
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    input.style.borderColor = '#e74c3c';
    input.focus();
    var errMsg = form.querySelector('.waitlist-err');
    if (!errMsg) {
      errMsg = document.createElement('span');
      errMsg.className = 'waitlist-err';
      errMsg.style.cssText = 'font-size:0.8rem;color:#e74c3c;display:block;margin-top:6px;';
      form.insertAdjacentElement('afterend', errMsg);
    }
    errMsg.textContent = 'Please enter a valid email address.';
    return;
  }

  // Clear any prior error state
  input.style.borderColor = '';
  var existingErr = form.nextElementSibling;
  if (existingErr && existingErr.classList.contains('waitlist-err')) {
    existingErr.textContent = '';
  }

  var originalText = btn.textContent;
  btn.textContent = 'Saving\u2026';
  btn.disabled = true;

  // TODO: replace URL below with the real API endpoint once backend supports it
  // The submit-review endpoint pattern (https://app.lingograde.com/api/submit-review)
  // is used as the reference; add /waitlist when the route exists.
  fetch('https://app.lingograde.com/api/waitlist', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email, product: product, source: 'shop' })
  })
  .then(function(r) {
    if (r.ok) {
      onWaitlistSuccess(btn, input, email, product);
    } else {
      throw new Error('Server error ' + r.status);
    }
  })
  .catch(function() {
    // Backend not yet available — persist locally as a fallback so no signup is lost
    var key = 'lg_waitlist';
    var existing = [];
    try { existing = JSON.parse(localStorage.getItem(key) || '[]'); } catch(e) {}
    var duplicate = existing.some(function(e) { return e.email === email && e.product === product; });
    if (!duplicate) {
      existing.push({ email: email, product: product, source: 'shop', ts: new Date().toISOString() });
      try { localStorage.setItem(key, JSON.stringify(existing)); } catch(e) {}
    }
    onWaitlistSuccess(btn, input, email, product);
  });
}

function onWaitlistSuccess(btn, input, email, product) {
  btn.textContent = 'You\u2019re on the list!';
  btn.style.background = '#27AE60';
  btn.disabled = true;
  input.disabled = true;
  input.value = email;
}

// ── GA4 client_id extraction (for server-side purchase attribution) ──
function getGaClientId() {
  try {
    var m = document.cookie.match(/_ga=GA\d+\.\d+\.(\d+\.\d+)/);
    return m ? m[1] : '';
  } catch (e) { return ''; }
}
window.getGaClientId = getGaClientId;

// ── Accessory Checkout via Stripe API ──
function toggleAccessoryForm(btn) {
  var form = btn.nextElementSibling;
  if (!form || !form.classList.contains('accessory-checkout-form')) return;
  var isOpen = form.style.maxHeight !== '0px' && form.style.maxHeight !== '';
  if (isOpen) {
    form.style.maxHeight = '0px';
  } else {
    form.style.maxHeight = '200px';
    var input = form.querySelector('.accessory-email');
    if (input) setTimeout(function() { input.focus(); }, 100);
  }
}

function checkoutAccessory(product, btn) {
  var form = btn.closest('.accessory-checkout-form');
  var input = form.querySelector('.accessory-email');
  var email = input ? input.value.trim() : '';

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    input.style.borderColor = '#e74c3c';
    input.focus();
    return;
  }
  input.style.borderColor = '';

  var originalText = btn.textContent;
  btn.textContent = 'Redirecting\u2026';
  btn.disabled = true;

  var API = window.LG_API || 'https://api.lingograde.com';
  fetch(API + '/v1/checkout/accessory', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email, product: product, ga_client_id: getGaClientId() })
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    if (data.checkout_url) {
      window.location.href = data.checkout_url;
    } else {
      btn.textContent = 'Something went wrong. Try again.';
      btn.disabled = false;
    }
  })
  .catch(function() {
    btn.textContent = 'Connection error. Try again.';
    btn.disabled = false;
  });
}
