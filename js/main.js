document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  document.querySelectorAll('.faq-item').forEach(function (item) {
    var q = item.querySelector('.faq-q');
    if (!q) return;
    q.addEventListener('click', function () {
      var isOpen = item.classList.contains('is-open');
      item.parentElement.querySelectorAll('.faq-item').forEach(function (el) {
        el.classList.remove('is-open');
        var btn = el.querySelector('.faq-q');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      });
      if (!isOpen) {
        item.classList.add('is-open');
        q.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // Gửi sự kiện GA4 khi khách bấm Gọi / Zalo, kèm vị trí nút được bấm
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="tel:"], a[href*="zalo.me"]');
    if (!link || typeof gtag !== 'function') return;
    var zones = [
      ['.mobile-cta', 'nut_noi_mobile'], ['.site-header', 'header'], ['.hero', 'banner_dau_trang'],
      ['.cta-band', 'khung_dat_xe'], ['.site-footer', 'footer']
    ];
    var location = 'noi_dung';
    for (var i = 0; i < zones.length; i++) {
      if (link.closest(zones[i][0])) { location = zones[i][1]; break; }
    }
    gtag('event', link.href.indexOf('tel:') === 0 ? 'click_call' : 'click_zalo', {
      link_location: location,
      page_path: window.location.pathname,
      transport_type: 'beacon'
    });
  });

  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
