DATE = "2026-11-27"
BASE = "https://www.thuexekiacarnival.vn"

# (tuyến, quãng đường, 1 chiều, khứ hồi, link, nhãn link, giá số cho schema)
ROUTES = [
    ("TP.HCM ⇄ Vũng Tàu", "95–120km", "2.000.000đ", "4.000.000đ", "/thue-xe-carnival-di-vung-tau.html", "Xe đi Vũng Tàu", 2000000),
    ("TP.HCM ⇄ Mộc Bài (Tây Ninh)", "70–75km", "2.000.000đ", "4.000.000đ", "/blog/thue-xe-carnival-di-cua-khau-moc-bai.html", "Kinh nghiệm Mộc Bài", 2000000),
    ("TP.HCM ⇄ Bến Tre", "85–90km", "2.400.000đ", "4.800.000đ", "/blog/kinh-nghiem-thue-xe-di-ben-tre.html", "Kinh nghiệm Bến Tre", 2400000),
    ("TP.HCM ⇄ Mũi Né (Phan Thiết)", "khoảng 200km", "2.500.000đ", "5.000.000đ", "/thue-xe-carnival-di-mui-ne.html", "Xe đi Mũi Né", 2500000),
    ("TP.HCM ⇄ Cần Thơ", "khoảng 170km", "3.000.000đ", "6.000.000đ", "/thue-xe-carnival-di-can-tho.html", "Xe đi Cần Thơ", 3000000),
    ("TP.HCM ⇄ Xa Mát (Tây Ninh)", "—", "3.000.000đ", "6.000.000đ", "/blog/kinh-nghiem-thue-xe-di-tay-ninh.html", "Kinh nghiệm Tây Ninh", 3000000),
    ("TP.HCM ⇄ Đà Lạt", "300–310km", "4.500.000đ", "Trọn gói 3N2Đ 10.000.000đ", "/thue-xe-carnival-di-da-lat.html", "Xe đi Đà Lạt", 4500000),
    ("TP.HCM ⇄ Rạch Giá", "khoảng 250km", "5.000.000đ", "10.000.000đ", "/blog/kinh-nghiem-thue-xe-di-rach-gia.html", "Kinh nghiệm Rạch Giá", 5000000),
    ("TP.HCM ⇄ Bạc Liêu", "khoảng 280km", "5.000.000đ", "10.000.000đ", "/blog/kinh-nghiem-thue-xe-di-bac-lieu-ca-mau.html", "Kinh nghiệm Bạc Liêu", 5000000),
    ("TP.HCM ⇄ Cà Mau", "khoảng 350km", "5.000.000đ", "10.000.000đ", "/blog/kinh-nghiem-thue-xe-di-bac-lieu-ca-mau.html", "Kinh nghiệm Cà Mau", 5000000),
    ("TP.HCM ⇄ Nha Trang", "440–450km", "5.500.000đ", "11.000.000đ", "/blog/kinh-nghiem-thue-xe-di-nha-trang.html", "Kinh nghiệm Nha Trang", 5500000),
]
OTHER = [
    ("Mỹ Tho", "khoảng 70km", "/blog/thue-xe-di-my-tho.html"),
    ("Vĩnh Long", "khoảng 135km", "/blog/kinh-nghiem-thue-xe-di-vinh-long.html"),
    ("Sóc Trăng", "khoảng 230km", "/blog/kinh-nghiem-thue-xe-di-soc-trang.html"),
    ("Châu Đốc (An Giang)", "khoảng 250km", "/blog/kinh-nghiem-thue-xe-di-chau-doc-an-giang.html"),
    ("Long Hải – Hồ Tràm", "—", "/blog/kinh-nghiem-thue-xe-di-long-hai-ho-tram.html"),
    ("Bảo Lộc", "—", "/blog/thue-xe-di-bao-loc.html"),
    ("Bình Dương", "—", "/blog/thue-xe-7-cho-di-binh-duong.html"),
    ("Củ Chi", "—", "/blog/thue-xe-di-dia-dao-cu-chi.html"),
    ("Cần Giờ", "—", "/blog/thue-xe-di-can-gio.html"),
]

rows = "\n".join(
    f'<tr><td>{r}</td><td>{km}</td><td>{a}</td><td>{b}</td><td><a href="{u}">{lbl}</a></td></tr>'
    for r, km, a, b, u, lbl, _ in ROUTES)
other_rows = "\n".join(f'<tr><td>{r}</td><td>{km}</td><td><a href="{u}">Xem kinh nghiệm</a></td></tr>' for r, km, u in OTHER)

SECTIONS = f"""
<section class="section">
  <div class="container">
    <div class="section-head">
      <div>
        <span class="eyebrow">Giá theo tuyến</span>
        <h2 class="h2">Bảng Giá Thuê Xe Carnival Đi Tỉnh Có Tài Xế</h2>
      </div>
      <a href="/bang-gia.html" class="btn btn--outline">Bảng Giá Tổng</a>
    </div>
    <div class="table-scroll"><table class="rate-table">
<thead><tr><th>Tuyến</th><th>Quãng đường</th><th>1 chiều</th><th>Khứ hồi trong ngày</th><th>Chi tiết</th></tr></thead>
<tbody>
{rows}
</tbody>
    </table></div>
    <p style="margin-top:16px; font-size:14px; color:var(--text-muted);">Giá 1 chiều là mức tối thiểu tham khảo cho xe Kia Carnival 7–8 chỗ có tài xế, đã gồm tài xế, nhiên liệu và bảo hiểm. Khứ hồi trong ngày bằng 2 lần giá 1 chiều. Quãng đường lấy theo điểm đón trong nội thành TP.HCM.</p>
  </div>
</section>

<section class="section section--panel">
  <div class="container">
    <div class="prose" style="max-width:820px;">
      <h2>Các tuyến khác: báo giá theo lịch trình</h2>
      <p>Những tuyến dưới đây được báo giá theo lịch trình thực tế (số điểm dừng, có ở lại qua đêm hay không). Với chuyến đi gần trong ngày, gói <a href="/thue-xe-theo-ngay.html">thuê xe theo ngày</a> 2.500.000đ cho 10 giờ/100km cộng phần vượt km 10.000đ/km thường là cách tính đơn giản nhất.</p>
      <div class="table-scroll"><table class="rate-table">
<thead><tr><th>Điểm đến</th><th>Quãng đường</th><th>Kinh nghiệm</th></tr></thead>
<tbody>
{other_rows}
</tbody>
      </table></div>

      <h2>Giá thuê xe đi tỉnh đã gồm những gì?</h2>
      <ul>
        <li><strong>Đã gồm:</strong> xe Kia Carnival đời 2023–2024, tài xế riêng, nhiên liệu và bảo hiểm.</li>
        <li><strong>Tính riêng theo thực tế:</strong> vé cầu đường, phà và phí gửi xe dọc đường.</li>
        <li><strong>Phụ thu:</strong> khung 22h–6h phụ thu 20% trên bảng giá.</li>
        <li><strong>Đặt cọc:</strong> 30% giá trị chuyến; hủy miễn phí trước 6 giờ khởi hành.</li>
      </ul>

      <h2>Nên chọn 1 chiều, khứ hồi hay trọn gói?</h2>
      <ul>
        <li><strong>1 chiều:</strong> đưa người thân về quê, ra sân bay tỉnh, hoặc đi một chiều rồi về bằng phương tiện khác.</li>
        <li><strong>Khứ hồi trong ngày:</strong> các tuyến dưới khoảng 200km như Vũng Tàu, Bến Tre, Mộc Bài, Mũi Né, Cần Thơ — đi sáng về tối.</li>
        <li><strong>Trọn gói nhiều ngày:</strong> Đà Lạt 3 ngày 2 đêm 10.000.000đ; các tuyến khác gọi để được báo giá theo số ngày.</li>
        <li><strong>Tự lái:</strong> nếu trong đoàn có người lái quen xe lớn, <a href="/thue-xe-tu-lai.html">thuê xe Carnival tự lái</a> 1.800.000đ/ngày, định mức 300km/ngày, cộng dồn theo số ngày thuê.</li>
      </ul>

      <h2>Kinh nghiệm đặt xe đi tỉnh dịp cao điểm</h2>
      <p>Cuối tuần, lễ 30/4, 2/9 và Tết là lúc xe 7 chỗ kín lịch nhanh nhất. Nên đặt trước 1–2 tuần với lễ thường và 3–4 tuần với Tết; gửi rõ điểm đón, giờ đi, số người và hành lý để được báo giá chính xác. Đi về quê dịp Tết, xem thêm <a href="/blog/kinh-nghiem-thue-xe-ve-que-tet.html">kinh nghiệm thuê xe về quê Tết</a>.</p>
    </div>
  </div>
</section>
"""

FAQS = [
    ("Thuê xe Carnival đi tỉnh giá bao nhiêu?", "Giá 1 chiều tham khảo: Vũng Tàu, Mộc Bài 2.000.000đ; Bến Tre 2.400.000đ; Mũi Né 2.500.000đ; Cần Thơ, Xa Mát 3.000.000đ; Đà Lạt 4.500.000đ; Rạch Giá, Bạc Liêu, Cà Mau 5.000.000đ; Nha Trang 5.500.000đ. Khứ hồi trong ngày bằng 2 lần giá 1 chiều."),
    ("Giá đã gồm xăng dầu và tài xế chưa?", "Đã gồm tài xế, nhiên liệu và bảo hiểm. Vé cầu đường, phà, gửi xe tính riêng theo thực tế; khung 22h–6h phụ thu 20%."),
    ("Đi Đà Lạt nhiều ngày tính thế nào?", "Có gói trọn 3 ngày 2 đêm 10.000.000đ; đưa hoặc đón 1 chiều 4.500.000đ. Tuyến Đà Lạt không có gói khứ hồi trong ngày do quãng đường xa."),
    ("Tuyến không có trong bảng thì sao?", "Gọi hoặc nhắn Zalo 090.6868.764 kèm điểm đón, điểm đến và số ngày; chúng tôi báo giá trong khoảng 5 phút."),
]

OFFERS = [{"@type": "Offer", "name": f"Thuê xe Kia Carnival có tài xế {r.replace('⇄', '-')} 1 chiều", "price": str(v), "priceCurrency": "VND"} for r, _, _, _, _, _, v in ROUTES]

PAGES = [{
    "slug": "bang-gia-thue-xe-carnival-di-tinh",
    "seo_title": "Bảng Giá Thuê Xe Carnival Đi Tỉnh 2026 | Có Tài Xế",
    "desc": "Bảng giá thuê xe Kia Carnival đi tỉnh 2026 có tài xế: Vũng Tàu 2tr, Mũi Né 2,5tr, Cần Thơ 3tr, Đà Lạt, Nha Trang, miền Tây. Đã gồm dầu. 090.6868.764.",
    "h1": "Bảng Giá Thuê Xe Carnival<br>Đi Tỉnh 2026", "h1_plain": "Bảng Giá Thuê Xe Carnival Đi Tỉnh 2026",
    "crumb": "Giá thuê xe đi tỉnh", "eyebrow": "Có tài xế · Đi tỉnh",
    "lede": "Giá thuê xe Kia Carnival 7–8 chỗ có tài xế từ TP.HCM đi các tỉnh, cập nhật 2026: một bảng cho mọi tuyến biển, miền Tây, Tây Nguyên. Giá đã gồm tài xế và nhiên liệu, khứ hồi trong ngày bằng 2 lần giá 1 chiều.",
    "image": "ngoai-that-sau-01", "alt": "Kia Carnival có tài xế với cốp rộng, sẵn sàng cho chuyến đi tỉnh từ TP.HCM",
    "sections": SECTIONS,
    "faq_title": "Câu Hỏi Về Giá Thuê Xe Đi Tỉnh",
    "faqs": FAQS,
    "extra_ld": [{
        "@context": "https://schema.org", "@type": "Service",
        "name": "Thuê xe Kia Carnival có tài xế đi tỉnh", "serviceType": "Thuê xe có tài xế đi tỉnh",
        "url": f"{BASE}/bang-gia-thue-xe-carnival-di-tinh.html",
        "provider": {"@type": "AutoRental", "@id": f"{BASE}/#business", "name": "Thuê Xe Kia Carnival VIP", "telephone": "+84906868764"},
        "areaServed": "Việt Nam",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Giá thuê xe Carnival đi tỉnh 2026", "itemListElement": OFFERS},
    }],
    "guides": [
        ("/thue-xe-7-cho-di-mien-tay.html", "Tuyến", "Thuê xe 7 chỗ đi miền Tây"),
        ("/blog/thue-xe-carnival-di-cong-tac-tinh.html", "Cẩm nang", "Thuê xe Carnival đi công tác tỉnh"),
        ("/blog/kinh-nghiem-thue-xe-di-phan-thiet.html", "Cẩm nang", "Kinh nghiệm thuê xe Carnival đi Phan Thiết"),
        ("/blog/kinh-nghiem-thue-xe-ve-que-tet.html", "Cẩm nang", "Kinh nghiệm thuê xe về quê Tết"),
    ],
    "cta_eyebrow": "Báo giá tuyến riêng", "cta_title": "Gửi Lộ Trình, Nhận Giá Trong 5 Phút",
}]
