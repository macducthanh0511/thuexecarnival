"""Sinh trang dịch vụ theo khu vực (quận) từ file dữ liệu.

Cách dùng:  python -X utf8 tools/area_tool.py tools/data/<file>.py
File dữ liệu định nghĩa PAGES (list dict). Khung trang (head, header, footer) lấy từ
thue-xe-carnival-tan-binh.html nên luôn đồng bộ với giao diện hiện tại.
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.thuexekiacarnival.vn"
TEMPLATE = ROOT / "thue-xe-carnival-tan-binh.html"
LANDSCAPE = {"ngoai-that-goc-34-01", "ngoai-that-goc-34-02", "ngoai-that-goc-34-03", "ngoai-that-goc-34-04",
             "ngoai-that-nghieng-01", "noi-that-ghe-hang2-02", "noi-that-ghe-hang2-03", "noi-that-taplo-01"}
ADDRESS = {"@type": "PostalAddress", "streetAddress": "2B Bàu Bàng", "addressLocality": "Phường Tân Bình",
           "addressRegion": "TP. Hồ Chí Minh", "addressCountry": "VN"}

SELF_DRIVE_CARDS = [
    ("/thue-xe-tu-lai.html", "🔑", "Giá Tự Lái", "1.800.000đ<br>/ngày, 300km"),
    ("/blog/dieu-kien-giay-to-thue-xe-tu-lai.html", "🪪", "Giấy Tờ", "CCCD gắn chip<br>+ GPLX hạng B"),
    ("/blog/kinh-nghiem-thue-xe-tu-lai-tranh-mat-coc.html", "💳", "Đặt Cọc", "15.000.000đ hoặc<br>thế chấp xe máy/sổ đỏ"),
    ("/lien-he.html", "🚚", "Giao Nhận Xe", "Tận nơi hoặc tại<br>2B Bàu Bàng"),
]
DRIVER_CARDS = [
    ("/thue-xe-theo-gio.html", "⏱️", "Theo Giờ", "450.000đ<br>tối thiểu 4h/40km"),
    ("/thue-xe-theo-ngay.html", "📅", "Theo Ngày", "2.500.000đ<br>10h/100km"),
    ("/thue-xe-dai-han.html", "🗓️", "Dài Hạn", "60.000.000đ<br>/tháng"),
    ("/thue-xe-tu-lai.html", "🔑", "Tự Lái", "1.800.000đ<br>/ngày, 300km"),
]


def save(path, text):
    nl = "\r\n" if path.exists() and b"\r\n" in path.read_bytes() else "\n"
    path.write_text(text, encoding="utf-8", newline=nl)


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def render(p):
    tpl = TEMPLATE.read_text(encoding="utf-8").replace("\r\n", "\n")
    head_start = tpl[:tpl.index("<title>")]
    header = tpl[tpl.index("</head>"):tpl.index('<nav class="breadcrumb">')]
    footer = tpl[tpl.index('<footer class="site-footer">'):]
    url = f"{BASE}/{p['slug']}.html"
    img = p["image"]
    w, h = (1276, 956) if img in LANDSCAPE else (956, 1276)
    self_drive = p["kind"] == "tu-lai"
    ld = [
        {"@context": "https://schema.org", "@type": "Service", "serviceType": p["service_type"],
         "name": p["h1_plain"], "url": url,
         "provider": {"@type": "AutoRental", "@id": f"{BASE}/#business", "name": "Thuê Xe Kia Carnival VIP",
                      "telephone": "+84906868764", "address": ADDRESS},
         "areaServed": {"@type": "Place", "name": f"{p['area']}, TP. Hồ Chí Minh"},
         "image": f"{BASE}/images/xe/{img}.jpg",
         "offers": {"@type": "Offer", "price": "1800000" if self_drive else "2500000", "priceCurrency": "VND",
                    "description": "Thuê xe Kia Carnival tự lái theo ngày, 300km/ngày" if self_drive
                    else "Thuê xe Kia Carnival có tài xế theo ngày, 10 giờ/100km"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Dịch vụ", "item": f"{BASE}/dich-vu.html"},
            {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url}]},
    ]
    ld_html = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>' for x in ld)
    head = f"""<title>{p['seo_title']}</title>
<meta name="description" content="{esc(p['desc'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(p['h1_plain'])}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/images/xe/{img}.jpg">
<meta property="og:locale" content="vi_VN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/images/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/bevietnampro-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/bevietnampro-400-vietnamese.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/oswald-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/style.css">
{ld_html}
"""
    cards = SELF_DRIVE_CARDS if self_drive else DRIVER_CARDS
    if not self_drive and p.get("tu_lai_url"):
        cards = [(p["tu_lai_url"] if c[0] == "/thue-xe-tu-lai.html" else c[0],) + c[1:] for c in cards]
    cards_html = "\n".join(
        f'      <a href="{u}" class="card">\n        <div class="card-icon">{i}</div>\n        <h3>{t}</h3>\n        <p>{d}</p>\n      </a>'
        for u, i, t, d in cards)
    routes = "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in p["routes"])
    faqs = "\n".join(
        f'      <div class="faq-item{" is-open" if n == 0 else ""}">\n'
        f'        <button class="faq-q" aria-expanded="{"true" if n == 0 else "false"}">{q}</button>\n'
        f'        <div class="faq-a"><p>{a}</p></div>\n      </div>' for n, (q, a) in enumerate(p["faqs"]))
    near = "\n".join(f'      <a href="{u}" class="related-guide"><span>{k}</span>{t}</a>' for u, k, t in p["nearby"])
    guides = "\n".join(f'      <a href="/blog/{s}.html" class="related-guide"><span>Cẩm nang</span>{t}</a>' for s, t in p["guides"])
    body = f"""<nav class="breadcrumb"><div class="container"><ul>
  <li><a href="/">Trang chủ</a></li>
  <li><a href="/dich-vu.html">Dịch vụ</a></li>
  <li>{p['crumb']}</li>
</ul></div></nav>

<section class="hero" style="padding-block:10px;">
  <div class="container two-col" style="padding-block:56px; align-items:center;">
    <div>
      <span class="eyebrow">{p['eyebrow']}</span>
      <h1 class="h1" style="margin-top:16px; font-size:clamp(2rem,4vw,3.2rem);">{p['h1']}</h1>
      <p class="lede" style="margin-top:18px;">{p['lede']}</p>
      <div class="hero-actions">
        <a href="tel:0906868764" class="btn btn--ember">Gọi Ngay: 090.6868.764</a>
        <a href="https://zalo.me/0906868764" class="btn btn--ghost" target="_blank" rel="noopener">Nhắn Zalo</a>
      </div>
    </div>
    <div class="photo-frame photo-frame--tall">
      <picture>
        <source type="image/webp" srcset="/images/xe/{img}-480.webp 480w, /images/xe/{img}-800.webp 800w, /images/xe/{img}-full.webp {w}w" sizes="(max-width:980px) 100vw, 50vw">
        <img src="/images/xe/{img}.jpg" alt="{esc(p['alt'])}" width="{w}" height="{h}" loading="eager" fetchpriority="high" decoding="async">
      </picture>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <div>
        <span class="eyebrow">{'Điều kiện &amp; giá' if self_drive else 'Bảng giá tham khảo'}</span>
        <h2 class="h2">{p['cards_title']}</h2>
      </div>
      <a href="/bang-gia.html" class="btn btn--outline">Bảng Giá Đầy Đủ</a>
    </div>
    <div class="grid grid--4">
{cards_html}
    </div>
  </div>
</section>

<section class="section section--panel">
  <div class="container">
    <div class="prose" style="max-width:820px;">
{p['body'].strip()}
      <h2>{p['routes_title']}</h2>
      <div class="table-scroll"><table class="rate-table">
<thead><tr><th>Điểm đến</th><th>Hướng đi</th><th>Gợi ý</th></tr></thead>
<tbody>
{routes}
</tbody>
      </table></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <div>
        <span class="eyebrow">Giải đáp</span>
        <h2 class="h2">{p['faq_title']}</h2>
      </div>
    </div>
    <div style="max-width:820px;">
{faqs}
    </div>
  </div>
</section>

<section class="section section--tight section--panel">
  <div class="container">
    <span class="eyebrow">Khu vực &amp; dịch vụ liên quan</span>
    <h2 class="h2" style="margin-top:12px;">Bạn Cũng Có Thể Cần</h2>
    <div class="related-guides__grid">
{near}
    </div>
  </div>
</section>

<!-- internal-links:start -->
<section class="section section--tight related-guides">
  <div class="container">
    <span class="eyebrow">Cẩm nang thuê xe</span>
    <h2 class="h2" style="margin-top:12px;">Bài Viết Hữu Ích Cho Bạn</h2>
    <div class="related-guides__grid">
{guides}
    </div>
  </div>
</section>
<!-- internal-links:end -->

<section class="cta-band">
  <div class="container">
    <span class="eyebrow" style="justify-content:center;">{p['cta_eyebrow']}</span>
    <h2 class="h2" style="margin-top:16px;">{p['cta_title']}</h2>
    <a href="tel:0906868764" class="btn btn--ember">Gọi 090.6868.764</a>
  </div>
</section>

"""
    return head_start + head + header + body + footer


def update_sitemap(pages, date):
    sm = ROOT / "sitemap.xml"
    t = sm.read_text(encoding="utf-8")
    add = ""
    for p in pages:
        loc = f"{BASE}/{p['slug']}.html"
        if loc not in t:
            add += f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{date}</lastmod>\n    <priority>0.7</priority>\n  </url>\n"
    if add:
        save(sm, t.replace("</urlset>", add + "</urlset>"))


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("data", sys.argv[1])
    data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data)
    for p in data.PAGES:
        assert len(p["seo_title"]) <= 60, (p["slug"], len(p["seo_title"]))
        assert len(p["desc"]) <= 155, (p["slug"], len(p["desc"]))
        save(ROOT / f"{p['slug']}.html", render(p))
        print("wrote", p["slug"])
    update_sitemap(data.PAGES, data.DATE)
