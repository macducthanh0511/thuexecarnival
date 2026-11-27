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

  // Hiệu ứng chỉ bật sau khi trang đã tải xong và trình duyệt rảnh,
  // để không chiếm CPU lúc trang đang hiển thị lần đầu.
  function startMotion() {
    var idle = window.requestIdleCallback || function (cb) { return setTimeout(cb, 200); };
    idle(initMotion, { timeout: 2000 });
  }
  if (document.readyState === 'complete') startMotion();
  else window.addEventListener('load', startMotion);
});

/* ===== Hiệu ứng cuộn trang ===== */
function initMotion() {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;
  var root = document.documentElement;

  // Gom phần tử cần hiệu ứng; bỏ qua banner và mọi thứ đang nằm trên màn hình
  // (đọc vị trí một lượt rồi mới ghi, tránh tính lại bố cục nhiều lần)
  var groups = [
    ['.section-head', ''], ['.card', ''], ['.price-card', ''], ['.step', ''], ['.testi', ''],
    ['.faq-item', ''], ['.info-line', 'left'], ['.badge-list span', ''],
    ['.photo-frame', 'photo'], ['.post-gallery figure', 'photo'], ['.related-guide', ''],
    ['.prose h2', 'left'], ['.prose table', ''], ['.cta-band .container', '']
  ];
  var vh = window.innerHeight, picked = [];
  groups.forEach(function (g) {
    document.querySelectorAll(g[0]).forEach(function (el) {
      if (el.closest('.hero') || el.closest('.site-header') || el.closest('.showcase')) return;
      picked.push([el, g[1]]);
    });
  });
  var below = picked.filter(function (x) { return x[0].getBoundingClientRect().top > vh; });

  root.classList.add('js-motion');
  // Thanh tiến độ đọc
  var bar = document.createElement('div');
  bar.className = 'scroll-progress';
  bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  below.forEach(function (x) { x[0].setAttribute('data-reveal', x[1]); });
  // Lệch nhịp cho các phần tử cùng hàng
  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    var sib = el.parentElement ? Array.prototype.filter.call(el.parentElement.children, function (c) { return c.hasAttribute('data-reveal'); }) : [];
    var idx = sib.indexOf(el);
    if (idx > 0) el.style.setProperty('--d', Math.min(idx, 6) * 0.08 + 's');
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px 12% 0px', threshold: 0 });
  document.querySelectorAll('[data-reveal]').forEach(function (el) { io.observe(el); });

  // Số đếm tăng dần
  var counters = Array.prototype.filter.call(document.querySelectorAll('.stat-num'), function (c) {
    return c.getBoundingClientRect().top > vh;
  });
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      cio.unobserve(en.target);
      var el = en.target, txt = el.textContent.trim();
      var m = txt.match(/^([\d.]+)(\+?)$/);
      if (!m) return;
      var target = parseInt(m[1].replace(/\./g, ''), 10), start = null;
      function step(ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / 1400, 1), e = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * e).toLocaleString('vi-VN') + m[2];
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }, { threshold: 0.6 });
  counters.forEach(function (c) { cio.observe(c); });

  // Parallax ảnh và showcase cuộn ngang
  var layers = Array.prototype.slice.call(document.querySelectorAll('.photo-frame[data-reveal] picture, [data-parallax]'));
  var showcase = document.querySelector('.showcase');
  var track = showcase && showcase.querySelector('.showcase__track');
  var ghost = showcase && showcase.querySelector('.showcase__ghost');
  var items = track ? Array.prototype.slice.call(track.children) : [];
  var desktop = window.matchMedia('(min-width: 981px)');
  var supportsScrollTimeline = window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()');
  var travel = 0, ticking = false, headerH = 0;
  var siteHeader = document.querySelector('.site-header');
  var sticky = showcase && showcase.querySelector('.showcase__sticky');

  function measure() {
    if (!showcase) return;
    if (desktop.matches) {
      var pos = siteHeader ? getComputedStyle(siteHeader).position : '';
      headerH = (pos === 'sticky' || pos === 'fixed') ? siteHeader.offsetHeight : 0;
      travel = Math.max(0, track.scrollWidth - window.innerWidth + 64);
      sticky.style.top = headerH + 'px';
      sticky.style.height = (window.innerHeight - headerH) + 'px';
      showcase.style.height = (window.innerHeight - headerH + travel) + 'px';
      showcase.classList.add('is-pinned');
    } else {
      showcase.style.height = '';
      sticky.style.top = '';
      sticky.style.height = '';
      showcase.classList.remove('is-pinned');
      track.style.transform = '';
    }
  }

  function frame() {
    ticking = false;
    var vh = window.innerHeight;
    if (!supportsScrollTimeline) {
      var max = document.documentElement.scrollHeight - vh;
      bar.style.transform = 'scaleX(' + (max > 0 ? window.scrollY / max : 0) + ')';
    }
    for (var i = 0; i < layers.length; i++) {
      var r = layers[i].getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) continue;
      var speed = parseFloat(layers[i].getAttribute('data-parallax')) || 0.08;
      var off = (r.top + r.height / 2 - vh / 2) * -speed;
      layers[i].style.transform = 'translate3d(0,' + off.toFixed(1) + 'px,0)';
    }
    if (showcase && desktop.matches) {
      var sr = showcase.getBoundingClientRect();
      var p = Math.min(Math.max((headerH - sr.top) / Math.max(travel, 1), 0), 1);
      track.style.transform = 'translate3d(' + (-p * travel).toFixed(1) + 'px,0,0)';
      if (ghost) ghost.style.transform = 'translate3d(' + (-p * travel * 0.35).toFixed(1) + 'px,0,0)';
      var cx = window.innerWidth / 2;
      items.forEach(function (it) {
        var ir = it.getBoundingClientRect();
        var d = Math.min(Math.abs(ir.left + ir.width / 2 - cx) / cx, 1);
        it.style.setProperty('--depth', d.toFixed(3));
      });
    }
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }

  measure();
  frame();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { measure(); onScroll(); });
  window.addEventListener('load', function () { measure(); onScroll(); });

  // Thẻ ảnh banner nghiêng nhẹ theo con trỏ (chỉ máy tính)
  var tilt = document.querySelector('.hero .gauge-card');
  if (tilt && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var hero = document.querySelector('.hero');
    hero.addEventListener('mousemove', function (e) {
      var r = tilt.getBoundingClientRect();
      var x = (e.clientX - (r.left + r.width / 2)) / r.width;
      var y = (e.clientY - (r.top + r.height / 2)) / r.height;
      tilt.style.transform = 'perspective(1000px) rotateY(' + (x * 7).toFixed(2) + 'deg) rotateX(' + (-y * 7).toFixed(2) + 'deg)';
    });
    hero.addEventListener('mouseleave', function () { tilt.style.transform = ''; });
  }
}
