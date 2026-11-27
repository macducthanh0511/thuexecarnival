"""Sinh bài blog theo khuôn site + cập nhật blog index, sitemap, lịch đăng bài và internal link.

Cách dùng:  python -X utf8 tools/blog_tool.py tools/data/<file>.py
File data khai báo POSTS (list dict) và tùy chọn INBOUND = [(file_html, slug_moi), ...]
để gắn link từ trang/bài cũ sang bài mới. Thư mục tools/ không được deploy (.vercelignore).
"""
import importlib.util, json, re, sys, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.thuexekiacarnival.vn"
TEMPLATE = ROOT / "blog/thue-xe-di-bao-loc.html"
START, END = "<!-- internal-links:start -->", "<!-- internal-links:end -->"

# Anchor chứa từ khóa cho trang chính; mỗi bài chọn cố định 1 biến thể để anchor đa dạng
ANCHORS = {
    "/": ["Thuê xe 7 chỗ có tài xế TP.HCM", "Dịch vụ thuê xe 7 chỗ có tài xế", "Thuê xe Kia Carnival TP.HCM", "Cho thuê xe 7 chỗ tại TP.HCM"],
    "/dua-don-san-bay.html": ["Thuê xe đưa đón sân bay Tân Sơn Nhất", "Xe đón sân bay Tân Sơn Nhất 7 chỗ", "Đưa đón sân bay bằng xe 7 chỗ"],
    "/thue-xe-tu-lai.html": ["Thuê xe tự lái 7 chỗ TP.HCM", "Thuê Carnival tự lái", "Thuê xe tự lái TP.HCM"],
    "/thue-xe-theo-ngay.html": ["Thuê xe 7 chỗ theo ngày", "Thuê xe có tài xế theo ngày", "Gói thuê xe theo ngày"],
    "/thue-xe-dai-han.html": ["Thuê xe 7 chỗ theo tháng", "Thuê xe hợp đồng dài hạn", "Thuê xe tháng cho doanh nghiệp"],
    "/thue-xe-theo-gio.html": ["Thuê xe 7 chỗ theo giờ", "Thuê xe theo giờ TP.HCM", "Gói thuê xe theo giờ"],
    "/thue-xe-carnival-di-vung-tau.html": ["Thuê xe 7 chỗ đi Vũng Tàu", "Thuê xe đi Vũng Tàu có tài xế", "Xe Carnival đi Vũng Tàu"],
    "/thue-xe-carnival-di-da-lat.html": ["Thuê xe 7 chỗ đi Đà Lạt", "Thuê xe đi Đà Lạt trọn gói", "Xe Carnival đi Đà Lạt"],
    "/thue-xe-carnival-di-mui-ne.html": ["Thuê xe 7 chỗ đi Mũi Né", "Thuê xe đi Phan Thiết – Mũi Né", "Xe Carnival đi Mũi Né"],
    "/thue-xe-carnival-di-can-tho.html": ["Thuê xe 7 chỗ đi Cần Thơ", "Thuê xe đi Cần Thơ có tài xế", "Xe Carnival đi Cần Thơ"],
    "/thue-xe-7-cho-di-mien-tay.html": ["Thuê xe 7 chỗ đi miền Tây", "Bảng giá thuê xe đi miền Tây", "Thuê xe đi các tỉnh miền Tây"],
    "/bang-gia.html": ["Bảng giá thuê xe 7 chỗ", "Giá thuê xe Carnival", "Bảng giá thuê xe mới nhất"],
}
LABELS = {"/doi-xe.html": "Đội xe", "/dich-vu.html": "Tất cả dịch vụ", "/lien-he.html": "Liên hệ đặt xe"}

LANDSCAPE = {"ngoai-that-goc-34-01", "ngoai-that-goc-34-02", "ngoai-that-goc-34-03", "ngoai-that-goc-34-04",
             "ngoai-that-nghieng-01", "noi-that-ghe-hang2-02", "noi-that-ghe-hang2-03", "noi-that-taplo-01"}

# Ảnh xe thật chèn giữa bài (giống tools đã áp cho bài cũ)
CAP = {
    "ngoai-that-goc-34-01": "Kia Carnival VIP màu đen, xe được rửa sạch trước mỗi chuyến",
    "ngoai-that-goc-34-02": "Đầu xe Kia Carnival với lưới tản nhiệt lớn, đèn LED sắc nét",
    "ngoai-that-goc-34-03": "Góc 3/4 Kia Carnival VIP, phía sau là các toà nhà trung tâm TP.HCM",
    "ngoai-that-goc-34-04": "Kia Carnival VIP sẵn sàng khởi hành cho chuyến đi trong ngày",
    "ngoai-that-nghieng-01": "Thân xe dài, cửa trượt hai bên giúp lên xuống dễ dàng",
    "noi-that-ghe-hang2-01": "Ghế hàng 2 dạng captain seat bọc da cam đất, có bệ đỡ chân",
    "noi-that-ghe-hang2-02": "Hai ghế thương gia hàng 2 tách rời, ngả lưng thoải mái",
    "noi-that-ghe-hang2-03": "Lối đi giữa hai ghế hàng 2, ra vào hàng 3 không cần gập ghế",
    "noi-that-ghe-truoc-01": "Khoang trước bọc da, cửa kính lớn quan sát thoáng",
    "noi-that-khoang-cabin-01": "Nhìn từ cốp sau: ba hàng ghế, đủ chỗ cho 7-8 người",
    "noi-that-khoang-cabin-02": "Khoang hành khách nhìn từ hàng ghế 2, nội thất da cam đất",
    "noi-that-taplo-01": "Khoang lái Kia Carnival nhìn từ ghế tài xế",
}
EXT = ["ngoai-that-goc-34-01", "ngoai-that-goc-34-03", "ngoai-that-goc-34-04", "ngoai-that-nghieng-01", "ngoai-that-goc-34-02"]
INT = ["noi-that-ghe-hang2-01", "noi-that-ghe-hang2-02", "noi-that-ghe-hang2-03", "noi-that-ghe-truoc-01",
       "noi-that-khoang-cabin-01", "noi-that-khoang-cabin-02", "noi-that-taplo-01"]


def gallery_pic(i, sizes, loading="lazy"):
    w, h = (1276, 956) if i in LANDSCAPE else (956, 1276)
    return (f'<picture><source type="image/webp" srcset="/images/xe/{i}-480.webp 480w, /images/xe/{i}-800.webp 800w" sizes="{sizes}">'
            f'<img src="/images/xe/{i}.jpg" alt="{CAP[i]}" width="{w}" height="{h}" loading="{loading}" decoding="async"></picture>')


def gallery(slug, hero_img):
    k = zlib.crc32(slug.encode())
    ext = [e for e in EXT if e != hero_img]
    a = ext[k % len(ext)]
    b = INT[(k // 7) % len(INT)]
    return ('<div class="post-gallery">\n'
            f'  <figure>{gallery_pic(a, "(max-width:640px) 100vw, 470px")}<figcaption>{CAP[a]}</figcaption></figure>\n'
            f'  <figure>{gallery_pic(b, "(max-width:640px) 100vw, 340px")}<figcaption>{CAP[b]}</figcaption></figure>\n'
            '</div>\n')



def save(path, text):
    """Ghi file giữ nguyên kiểu xuống dòng (CRLF/LF) của file cũ."""
    nl = "\r\n" if path.exists() and b"\r\n" in path.read_bytes() else "\n"
    path.write_text(text, encoding="utf-8", newline=nl)


def dmy(d):
    y, m, dd = d.split("-")
    return f"{dd}/{m}/{y}"


def picture(p, sizes, loading="lazy"):
    i = p["image"]
    load = 'loading="eager" fetchpriority="high"' if loading == "eager" else 'loading="lazy"'
    w, h = (1276, 956) if i in LANDSCAPE else (956, 1276)
    return (f'<picture>\n            <source type="image/webp" srcset="/images/xe/{i}-480.webp 480w, /images/xe/{i}-800.webp 800w, /images/xe/{i}-full.webp {w}w" sizes="{sizes}">\n'
            f'            <img src="/images/xe/{i}.jpg" alt="{p["alt"]}" width="{w}" height="{h}" {load} decoding="async">\n          </picture>')


def title_of(slug):
    t = (ROOT / "blog" / f"{slug}.html").read_text(encoding="utf-8")
    return re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S).group(1)).strip()


def anchor(url, key):
    v = ANCHORS.get(url)
    return v[zlib.crc32(f"{key}|{url}".encode()) % len(v)] if v else LABELS.get(url, url)


def related_block(slug, related, services):
    services = services + (["/"] if "/" not in services else [])
    lis = "\n".join(f'          <li><a href="/blog/{r}.html">{title_of(r)}</a></li>' for r in related)
    svc = " · ".join(f'<a href="{u}">{anchor(u, slug)}</a>' for u in services)
    return f"""      {START}
      <aside class="related-posts" aria-label="Bài viết liên quan">
        <h2>Bài viết liên quan</h2>
        <ul>
{lis}
        </ul>
        <p class="related-services"><strong>Dịch vụ liên quan:</strong> {svc} · <a href="/blog/index.html">Xem tất cả bài viết</a></p>
      </aside>
      {END}
"""


def with_gallery(p):
    """Chèn cặp ảnh xe thật trước thẻ h2 thứ 3 của thân bài."""
    body = p["body"].strip()
    hs = [m.start() for m in re.finditer(r"<h2", body)]
    if len(hs) < 3:
        return body
    return body[:hs[2]] + gallery(p["slug"], p["image"]) + body[hs[2]:]


def render(p):
    tpl = TEMPLATE.read_text(encoding="utf-8")
    head_start = tpl[:tpl.index("<title>")]
    header = tpl[tpl.index("</head>"):tpl.index('<nav class="breadcrumb">')]
    tail = tpl[tpl.index("    </article>"):]
    url = f"{BASE}/blog/{p['slug']}.html"
    img = f"{BASE}/images/xe/{p['image']}.jpg"
    ld = [
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
         "datePublished": p["date"], "dateModified": p["date"],
         "author": {"@type": "Organization", "name": "Thuê Xe Kia Carnival VIP"},
         "publisher": {"@type": "Organization", "name": "Thuê Xe Kia Carnival VIP",
                       "logo": {"@type": "ImageObject", "url": f"{BASE}/images/favicon.svg"}},
         "mainEntityOfPage": url, "image": img, "keywords": p["keyword"]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/index.html"},
            {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url}]},
    ]
    ld_html = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>' for x in ld)
    faq_html = "\n".join(f"<h3>{q}</h3>\n<p>{a}</p>" for q, a in p["faqs"])
    head = f"""<title>{p['seo_title']}</title>
<meta name="description" content="{p['desc']}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['og_desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="vi_VN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/images/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/bevietnampro-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/bevietnampro-400-vietnamese.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/oswald-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/oswald-vietnamese.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/style.css">
{ld_html}
"""
    body = f"""<nav class="breadcrumb"><div class="container"><ul>
  <li><a href="/">Trang chủ</a></li>
  <li><a href="/blog/index.html">Blog</a></li>
  <li>{p['crumb']}</li>
</ul></div></nav>

<section class="section">
  <div class="container">
    <article class="prose" style="max-width:820px; margin-inline:auto;">
      <div class="post-meta">{p['category']} · {dmy(p['date'])} · {p['read']} phút đọc</div>
      <h1 class="h2" style="margin-top:14px; text-transform:none;">{p['title']}</h1>
      <div class="thumb" style="margin-top:26px; margin-bottom:8px;">
        {picture(p, "(max-width:640px) 100vw, 760px", "eager")}
      </div>
{with_gallery(p)}

<h2>Câu hỏi thường gặp</h2>
{faq_html}

"""
    # tail bắt đầu bằng khối related cũ của template -> bỏ, chèn khối mới
    tail = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", "", tail, flags=re.S)
    tail = tail.lstrip(" ")
    return head_start + head + header + body + related_block(p["slug"], p["related"], p["services"]) + "    " + tail


def update_index(posts):
    path = ROOT / "blog/index.html"
    idx = path.read_text(encoding="utf-8")
    for p in posts:
        if f'/blog/{p["slug"]}.html" class="blog-card"' in idx:
            continue
        card = f"""      <a href="/blog/{p['slug']}.html" class="blog-card">
        <div class="thumb">
          {picture(p, "(max-width:980px) 100vw, 33vw")}
        </div>
        <div class="post-meta">{p['category']} · {dmy(p['date'])}</div>
        <h3 style="margin-top:10px; margin-bottom:10px;">{p['title']}</h3>
        <p style="color:var(--text-muted); font-size:14.5px;">{p['card_desc']}</p>
      </a>
"""
        last = idx.rindex('class="blog-card"')
        pos = idx.index("    </div>\n  </div>\n</section>", last)
        idx = idx[:pos] + card + idx[pos:]
        entry = (',\n    {\n      "@type": "BlogPosting",\n'
                 f'      "headline": {json.dumps(p["title"], ensure_ascii=False)},\n'
                 f'      "url": "{BASE}/blog/{p["slug"]}.html",\n      "datePublished": "{p["date"]}",\n'
                 f'      "image": "{BASE}/images/xe/{p["image"]}.jpg"\n    }}')
        end = idx.index("\n  ]\n}\n</script>")
        idx = idx[:end] + entry + idx[end:]
    save(path, idx)


def update_sitemap(posts):
    path = ROOT / "sitemap.xml"
    sm = path.read_text(encoding="utf-8")
    for p in posts:
        loc = f"{BASE}/blog/{p['slug']}.html"
        if loc not in sm:
            sm = sm.replace("</urlset>", f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{p['date']}</lastmod>\n    <priority>0.6</priority>\n  </url>\n</urlset>")
    save(path, sm)


def update_calendar(posts):
    from copy import copy
    import openpyxl
    xp = ROOT / "Lich_Dang_Bai_SEO_ThueXeCarnival.xlsx"
    wb = openpyxl.load_workbook(xp)
    ws = wb.active
    have = {ws.cell(r, 7).value for r in range(2, ws.max_row + 1)}
    src = ws.max_row
    for p in posts:
        if f"{p['slug']}.html" in have:
            continue
        r = ws.max_row + 1
        for c, v in enumerate([dmy(p["date"]), p["title"], p["keyword"], p["intent"], p["category"], "Đã đăng", f"{p['slug']}.html"], 1):
            cell = ws.cell(r, c, v)
            if ws.cell(src, c).has_style:
                cell._style = copy(ws.cell(src, c)._style)
    wb.save(xp)


def add_inbound(page, slug):
    """Gắn link sang bài mới: vào khối 'Bài viết liên quan' (bài blog) hoặc 'Cẩm nang' (trang thường)."""
    path = ROOT / page
    t = path.read_text(encoding="utf-8")
    href = f'href="/blog/{slug}.html"'
    if href in t:
        return
    title = title_of(slug)
    if '<aside class="related-posts"' in t:
        i = t.index("        </ul>", t.index('<aside class="related-posts"'))
        t = t[:i] + f'          <li><a href="/blog/{slug}.html">{title}</a></li>\n' + t[i:]
    elif 'class="related-guides__grid"' in t:
        i = t.index("    </div>", t.index('class="related-guides__grid"'))
        t = t[:i] + f'      <a href="/blog/{slug}.html" class="related-guide"><span>Cẩm nang</span>{title}</a>\n' + t[i:]
    else:
        raise SystemExit(f"{page}: không có khối internal link")
    save(path, t)


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("data", sys.argv[1])
    data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data)
    for p in data.POSTS:
        assert len(p["seo_title"]) <= 60 and len(p["desc"]) <= 155, (p["slug"], len(p["seo_title"]), len(p["desc"]))
        save(ROOT / "blog" / f"{p['slug']}.html", render(p))
        print("wrote", p["slug"])
    update_index(data.POSTS)
    update_sitemap(data.POSTS)
    update_calendar(data.POSTS)
    for page, slug in getattr(data, "INBOUND", []):
        add_inbound(page, slug)
    print("index, sitemap, lịch đăng bài, inbound links: ok")
