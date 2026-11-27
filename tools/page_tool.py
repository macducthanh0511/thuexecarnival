"""Sinh trang dịch vụ/landing tự do (không theo khuôn quận) từ file dữ liệu.

Cách dùng:  python -X utf8 tools/page_tool.py tools/data/<file>.py
File dữ liệu định nghĩa PAGES (list dict) và DATE. Khung trang lấy từ thue-xe-carnival-tan-binh.html.
Mỗi page: slug, seo_title, desc, h1, h1_plain, crumb, eyebrow, lede, image, alt,
sections (HTML các <section> thân trang), faqs [(q, a)], faq_title, extra_ld [dict], guides [(slug, title)],
cta_eyebrow, cta_title.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from area_tool import ROOT, BASE, TEMPLATE, LANDSCAPE, save, esc, update_sitemap  # noqa: E402


def render(p):
    tpl = TEMPLATE.read_text(encoding="utf-8").replace("\r\n", "\n")
    head_start = tpl[:tpl.index("<title>")]
    header = tpl[tpl.index("</head>"):tpl.index('<nav class="breadcrumb">')]
    footer = tpl[tpl.index('<footer class="site-footer">'):]
    url = f"{BASE}/{p['slug']}.html"
    img = p["image"]
    w, h = (1276, 956) if img in LANDSCAPE else (956, 1276)
    ld = list(p.get("extra_ld", [])) + [
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
            for q, a in p["faqs"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Bảng giá", "item": f"{BASE}/bang-gia.html"},
            {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url}]},
    ]
    ld_html = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>' for x in ld)
    head_links = tpl[tpl.index('<link rel="icon"'):tpl.index('<script type="application/ld+json">')]
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
{head_links}{ld_html}
"""
    faqs = "\n".join(
        f'      <div class="faq-item{" is-open" if n == 0 else ""}">\n'
        f'        <button class="faq-q" aria-expanded="{"true" if n == 0 else "false"}">{q}</button>\n'
        f'        <div class="faq-a"><p>{a}</p></div>\n      </div>' for n, (q, a) in enumerate(p["faqs"]))
    guides = "\n".join(f'      <a href="{u}" class="related-guide"><span>{k}</span>{t}</a>' for u, k, t in p["guides"])
    body = f"""<nav class="breadcrumb"><div class="container"><ul>
  <li><a href="/">Trang chủ</a></li>
  <li><a href="/bang-gia.html">Bảng giá</a></li>
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
        <a href="https://zalo.me/0906868764" class="btn btn--ghost" target="_blank" rel="noopener">Nhắn Zalo Báo Giá</a>
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

{p['sections'].strip()}

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

<!-- internal-links:start -->
<section class="section section--tight related-guides">
  <div class="container">
    <span class="eyebrow">Kinh nghiệm theo tuyến</span>
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
