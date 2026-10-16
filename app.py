import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ===================== CẤU HÌNH TRANG =====================
st.set_page_config(
    page_title="Hỗ Trợ Trẻ Mầm Non — Phát Hiện & Can Thiệp Sớm",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Lấy API Key từ Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

# ===================== KHỞI TẠO DỮ LIỆU =====================
if 'danh_sach_tre' not in st.session_state:
    st.session_state.danh_sach_tre = []
if 'tre_hien_tai' not in st.session_state:
    st.session_state.tre_hien_tai = None

# ===================== TIÊU ĐỀ =====================
st.markdown("""
    <h1 style='text-align: center; color: #ff6b9d;'>🌸 Hỗ Trợ Trẻ Mầm Non — Phát Hiện & Can Thiệp Sớm</h1>
    <p style='text-align: center; color: #666; font-size: 17px;'>Theo dõi, đánh giá & xây dựng kế hoạch hỗ trợ cá nhân — Đặc biệt trẻ 25–36 tháng tuổi, trẻ rối loạn phổ tự kỷ</p>
    <hr style='border: 2px solid #ffd6e8; margin: 10px 0;'>
""", unsafe_allow_html=True)

# ===================== THANH BÊN TRÁI =====================
with st.sidebar:
    st.header("🎈 Menu chính")
    chuc_nang = st.radio("", [
        "👶 Quản lý hồ sơ trẻ",
        "📋 Đánh giá phát triển (ASQ-3)",
        "🔍 Sàng lọc rối loạn phổ tự kỷ",
        "📝 Xây dựng kế hoạch hỗ trợ",
        "📚 Thư viện hoạt động",
        "📥 Xuất báo cáo & kế hoạch"
    ])
    
    st.markdown("---")
    st.caption("💡 Dựa trên: ASQ-3, M-CHAT-R/F, Quyết định 2254/QĐ-BYT, Chương trình GD Mầm non")

# ===================== MODULE 1: HỒ SƠ TRẺ =====================
if chuc_nang == "👶 Quản lý hồ sơ trẻ":
    st.subheader("👶 Hồ sơ theo dõi trẻ")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        ten_tre = st.text_input("Tên trẻ")
        ngay_sinh = st.date_input("Ngày sinh")
        gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ"])
    with col2:
        ngay_vao_lop = st.date_input("Ngày vào lớp")
        ghi_chu_dac_biet = st.text_area("Ghi chú đặc biệt (nếu có)")
    
    if st.button("✅ Lưu hồ sơ", type="primary"):
        if ten_tre:
            tre_moi = {
                "ten": ten_tre,
                "ngay_sinh": ngay_sinh,
                "gioi_tinh": gioi_tinh,
                "ngay_vao_lop": ngay_vao_lop,
                "ghi_chu": ghi_chu_dac_biet,
                "ngay_tao": datetime.now().strftime("%d/%m/%Y")
            }
            st.session_state.danh_sach_tre.append(tre_moi)
            st.session_state.tre_hien_tai = tre_moi
            st.success(f"✅ Đã lưu hồ sơ: {ten_tre}")
        else:
            st.error("Vui lòng nhập tên trẻ!")
    
    st.markdown("---")
    st.subheader("📋 Danh sách trẻ")
    if st.session_state.danh_sach_tre:
        for idx, tre in enumerate(st.session_state.danh_sach_tre):
            with st.expander(f"👤 {tre['ten']} — {tre['ngay_sinh']}"):
                st.write(f"**Ngày sinh:** {tre['ngay_sinh']}")
                st.write(f"**Ghi chú:** {tre['ghi_chu'] or 'Không có'}")
                if st.button(f"Chọn theo dõi → {tre['ten']}", key=f"chon_{idx}"):
                    st.session_state.tre_hien_tai = tre
                    st.success(f"Đang theo dõi: {tre['ten']}")
                    st.rerun()
    else:
        st.info("ℹ️ Chưa có hồ sơ nào. Vui lòng thêm trẻ trước!")

# ===================== MODULE 2: ĐÁNH GIÁ ASQ-3 =====================
elif chuc_nang == "📋 Đánh giá phát triển (ASQ-3)":
    if not st.session_state.tre_hien_tai:
        st.warning("⚠️ Vui lòng chọn trẻ trong mục 'Quản lý hồ sơ' trước!")
    else:
        st.subheader(f"📋 Đánh giá phát triển — {st.session_state.tre_hien_tai['ten']} (25–36 tháng)")
        st.info("Dựa trên Bộ công cụ ASQ-3 — Đánh giá 5 lĩnh vực phát triển chính")
        
        linh_vuc = st.selectbox("Chọn lĩnh vực đánh giá", [
            "Giao tiếp",
            "Vận động to",
            "Vận động nhỏ",
            "Giải quyết vấn đề",
            "Cá nhân - Xã hội"
        ])
        
        st.markdown(f"### ✅ {linh_vuc}")
        st.write("Trả lời các câu hỏi sau dựa trên quan sát thực tế của trẻ:")
        
        cau_hoi = {
            "Giao tiếp": [
                "Trẻ có đáp ứng khi gọi tên không?",
                "Trẻ có chỉ đồ vật để chia sẻ sự chú ý không?",
                "Trẻ nói được bao nhiêu từ có nghĩa?"
            ],
            "Vận động to": [
                "Trẻ có chạy được không?",
                "Trẻ nhảy được bằng hai chân không?",
                "Trẻ đi lên xuống cầu thang không cần nắm không?"
            ],
            "Vận động nhỏ": [
                "Trẻ cầm bút chì đúng cách không?",
                "Trẻ xếp được khối chồng lên nhau không?",
                "Trẻ lật được từng trang sách không?"
            ],
            "Giải quyết vấn đề": [
                "Trẻ tìm được đồ vật bị che giấu không?",
                "Trẻ bắt chước được hành động người khác không?",
                "Trẻ thực hiện được yêu cầu đơn giản không?"
            ],
            "Cá nhân - Xã hội": [
                "Trẻ chơi cùng bạn được không?",
                "Trẻ tự ăn được với muỗng không?",
                "Trẻ thể hiện tình cảm với người thân không?"
            ]
        }
        
        dap_an = {}
        for ch in cau_hoi[linh_vuc]:
            dap_an[ch] = st.radio(ch, ["Có", "Đôi khi", "Chưa"], key=ch)
        
        if st.button("📊 Xem kết quả đánh giá", type="primary"):
            co = sum(1 for v in dap_an.values() if v == "Có")
            tong = len(dap_an)
            st.markdown(f"#### Kết quả: {co}/{tong} câu trả lời 'Có'")
            if co >= 2:
                st.success("✅ Phát triển phù hợp độ tuổi")
            elif co == 1:
                st.warning("⚠️ Cần theo dõi thêm")
            else:
                st.error("🔴 Cần chú ý — Giới thiệu chuyên môn sớm")

# ===================== MODULE 3: SÀNG LỌC TỰ KỶ =====================
elif chuc_nang == "🔍 Sàng lọc rối loạn phổ tự kỷ":
    if not st.session_state.tre_hien_tai:
        st.warning("⚠️ Vui lòng chọn trẻ trong mục 'Quản lý hồ sơ' trước!")
    else:
        st.subheader(f"🔍 Sàng lọc rối loạn phổ tự kỷ — {st.session_state.tre_hien_tai['ten']}")
        st.info("Dựa trên M-CHAT-R/F & Quyết định 2254/QĐ-BYT — Dành cho trẻ dưới 36 tháng")
        
        st.markdown("### Trả lời các câu hỏi sau:")
        st.markdown("*Chọn 'Có' hoặc 'Không' theo hành vi thực tế của trẻ*")
        
        dấu_hieu = [
            ("Khi bạn gọi tên trẻ, trẻ có ngẩng đầu/lại gần không?", False),
            ("Trẻ chỉ tay vào đồ vật để bạn xem cùng không?", False),
            ("Trẻ thích chơi giả vờ không?", False),
            ("Trẻ nhìn vào mắt bạn khi giao tiếp không?", False),
            ("Trẻ bắt chước hành động của bạn không?", False),
            ("Trẻ có nhìn chằm chằm vào đồ vật di chuyển không?", True),
            ("Trẻ lặp lại hành vi giống hệt nhiều lần không?", True),
            ("Trẻ không thích thay đổi thói quen không?", True)
        ]
        
        nguy_co = 0
        cau_hoi_danh_gia = {}
        for ch, la_dau_hieu in dấu_hieu:
            dap = st.radio(ch, ["Có", "Không"], key=f"aut_{ch[:10]}")
            cau_hoi_danh_gia[ch] = dap
            if la_dau_hieu and dap == "Có":
                nguy_co += 1
            if not la_dau_hieu and dap == "Không":
                nguy_co += 1
        
        if st.button("🔎 Xem kết quả sàng lọc", type="primary"):
            st.markdown("---")
            if nguy_co >= 3:
                st.error("""
                ### ⚠️ Có dấu hiệu nguy cơ — Cần giới thiệu chuyên môn
                Dựa trên kết quả sàng lọc, trẻ có một số dấu hiệu cần được đánh giá chi tiết hơn.
                - Thông báo cho gia đình
                - Giới thiệu đến bác sĩ/chuyên gia tâm lý giáo dục
                - Không chờ "lớn sẽ tự hết" — can thiệp sớm hiệu quả cao nhất
                """)
            elif nguy_co >= 1:
                st.warning("""
                ### 📋 Cần theo dõi định kỳ
                Có một vài điểm cần quan sát thêm. Tiếp tục theo dõi tại lớp và thông báo cho gia đình.
                Lặp lại sàng lọc sau 1–2 tháng.
                """)
            else:
                st.success("""
                ### ✅ Không có dấu hiệu bất thường rõ rệt
                Tiếp tục quan sát hàng ngày. Nếu có thay đổi bất thường, sàng lọc lại.
                """)

# ===================== MODULE 4: KẾ HOẠCH HỖ TRỢ CÁ NHÂN =====================
elif chuc_nang == "📝 Xây dựng kế hoạch hỗ trợ":
    if not st.session_state.tre_hien_tai:
        st.warning("⚠️ Vui lòng chọn trẻ trong mục 'Quản lý hồ sơ' trước!")
    elif not API_KEY:
        st.warning("⚠️ Chưa có khóa API. Vui lòng cấu hình GOOGLE_API_KEY trong Cài đặt nâng cao.")
    else:
        st.subheader(f"📝 Kế hoạch hỗ trợ cá nhân — {st.session_state.tre_hien_tai['ten']}")
        
        col1, col2 = st.columns(2)
        with col1:
            muc_tieu_ngan_han = st.text_area("🎯 Mục tiêu ngắn hạn (2–4 tuần)")
            diem_manh = st.text_area("⭐ Điểm mạnh của trẻ")
        with col2:
            can_ho_tro = st.text_area("🔍 Điểm cần hỗ trợ")
            phuong_phap = st.selectbox("Phương pháp chính", [
                "Từng bước nhỏ — củng cố tích cực",
                "Can thiệp hành vi tích cực",
                "Hỗ trợ giao tiếp bằng hình ảnh/AAC",
                "Kết hợp nhiều phương pháp"
            ])
        
        if st.button("🌸 Tạo kế hoạch hỗ trợ", type="primary"):
            with st.spinner("🔄 Đang xây dựng kế hoạch..."):
                try:
                    prompt = f"""
Bạn là chuyên gia giáo dục mầm non và can thiệp sớm. Xây dựng kế hoạch hỗ trợ cá nhân chi tiết cho trẻ:

=== THÔNG TIN TRẺ ===
- Tên: {st.session_state.tre_hien_tai['ten']}
- Độ tuổi: 25–36 tháng
- Điểm mạnh: {diem_manh if diem_manh else 'Chưa ghi nhận'}
- Điểm cần hỗ trợ: {can_ho_tro if can_ho_tro else 'Chưa ghi nhận'}
- Mục tiêu ngắn hạn: {muc_tieu_ngan_han if muc_tieu_ngan_han else 'Tự xây dựng phù hợp độ tuổi'}
- Phương pháp ưu tiên: {phuong_phap}

=== YÊU CẦU ===
1. Áp dụng nguyên tắc "Từng bước nhỏ": chia mỗi mục tiêu thành các bước dễ thực hiện
2. Hoạt động cụ thể, vật liệu dễ kiếm tại lớp & nhà
3. Phân biệt: hoạt động tại lớp, hoạt động phối hợp với gia đình
4. Cách đánh giá tiến độ đơn giản
5. Ngôn ngữ rõ ràng, dễ hiểu cho giáo viên & phụ huynh
6. Định dạng dễ đọc, dùng gạch đầu dòng

Viết bằng tiếng Việt, thân thiện, thực tế.
                    """
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    response = model.generate_content(prompt)
                    noi_dung = response.text
                    
                    st.success("✅ Kế hoạch đã được tạo!")
                    st.markdown("---")
                    st.markdown(noi_dung)
                    
                    st.session_state.current_file = {
                        "title": f"Kế hoạch hỗ trợ: {st.session_state.tre_hien_tai['ten']}",
                        "content": noi_dung,
                        "type": "Kế hoạch hỗ trợ"
                    }
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        st.error("⏳ Hết giới hạn yêu cầu hôm nay! Vui lòng thử lại sau hoặc đổi API Key.")
                    else:
                        st.error(f"❌ Lỗi: {str(e)}")

# ===================== MODULE 5: THƯ VIỆN HOẠT ĐỘNG =====================
elif chuc_nang == "📚 Thư viện hoạt động":
    st.subheader("📚 Thư viện hoạt động hỗ trợ — 25–36 tháng")
    
    loai_hoat_dong = st.selectbox("Chọn loại hoạt động", [
        "Giao tiếp & Ngôn ngữ",
        "Tương tác xã hội & Cảm xúc",
        "Nhận thức & Giác quan",
        "Vận động to & nhỏ",
        "Tự phục vụ & Kỹ năng sống",
        "Hoạt động chuyên biệt cho trẻ tự kỷ"
    ])
    
    thu_vien = {
        "Giao tiếp & Ngôn ngữ": [
            {"ten": "Trò chơi gọi tên", "muc_dich": "Khuyến khích trẻ đáp ứng khi gọi tên", "cach_lam": "Gọi tên trẻ, khen ngay khi trẻ đáp ứng. Tăng dần khoảng cách gọi."},
            {"ten": "Chỉ và nói", "muc_dich": "Rèn luyện ngôn ngữ biểu đạt", "cach_lam": "Chỉ vào đồ vật quen thuộc, nói tên. Khuyến khích trẻ bắt chước."},
            {"ten": "Sử dụng thẻ hình ảnh giao tiếp", "muc_dich": "Hỗ trợ trẻ khó nói biểu đạt nhu cầu", "cach_lam": "In hình ảnh đồ ăn, nước uống, chơi... Hướng dẫn trẻ chỉ vào thẻ khi có nhu cầu."}
        ],
        "Tương tác xã hội & Cảm xúc": [
            {"ten": "Chơi cùng bạn", "muc_dich": "Khuyến khích tương tác bạn bè", "cach_lam": "Tổ chức trò chơi đơn giản theo cặp: chuyền bóng, xếp khối cùng nhau."},
            {"ten": "Đọc cảm xúc trên mặt", "muc_dich": "Nhận biết biểu cảm cơ bản", "cach_lam": "Dùng thẻ hình mặt vui, buồn, giận... Hướng dẫn trẻ nhận biết và bắt chước."},
            {"ten": "Chia sẻ đồ chơi", "muc_dich": "Rèn luyện hành vi xã hội tích cực", "cach_lam": "Dạy trẻ đưa đồ chơi cho bạn, nhận lời khen khi chia sẻ."}
        ],
        "Hoạt động chuyên biệt cho trẻ tự kỷ": [
            {"ten": "Bảng lịch sử dụng hình ảnh", "muc_dich": "Giúp trẻ hiểu quy trình, giảm lo lắng thay đổi", "cach_lam": "In hình ảnh các hoạt động trong ngày: ăn, chơi, ngủ... Dán theo thứ tự. Thực hiện theo hình ảnh."},
            {"ten": "Thời gian chơi theo chu kỳ", "muc_dich": "Tạo sự ổn định, dự đoán được", "cach_lam": "Chia thời gian thành các khối nhỏ: 10 phút chơi tự chọn → 10 phút hoạt động hướng dẫn → nghỉ."},
            {"ten": "Hỗ trợ giác quan", "muc_dich": "Giảm quá tải giác quan", "cach_lam": "Góc yên tĩnh với gối mềm, vật liệu xúc giác an toàn. Cho trẻ vào khi quá nhạy cảm với tiếng ồn, ánh sáng."}
        ]
    }
    
    hien_thi = thu_vien.get(loai_hoat_dong, [
        {"ten": "Hoạt động mẫu", "muc_dich": "Đang cập nhật", "cach_lam": "Chọn danh mục khác để xem chi tiết"}
    ])
    
    for idx, hd in enumerate(hien_thi, 1):
        with st.expander(f"{idx}. {hd['ten']}"):
            st.write(f"**🎯 Mục đích:** {hd['muc_dich']}")
            st.write(f"**📝 Cách thực hiện:** {hd['cach_lam']}")
            st.write("**⭐ Lưu ý:** Điều chỉnh theo mức độ của từng trẻ. Bắt đầu từ bước đơn giản nhất, củng cố tích cực.")

# ===================== MODULE 6: XUẤT BÁO CÁO =====================
elif chuc_nang == "📥 Xuất báo cáo & kế hoạch":
    st.subheader("📥 Tải xuống kế hoạch & báo cáo")
    
    if 'current_file' in st.session_state and st.session_state.current_file:
        file_data = st.session_state.current_file
        st.markdown(f"### 📄 Tài liệu hiện tại: {file_data['title']}")
        st.markdown("---")
        st.markdown(file_data['content'])
        
        ten_file = file_data['title'].replace(":", "-").replace(" ", "_")
        st.download_button(
            label="📄 Tải xuống (.txt)",
            data=file_data['content'],
            file_name=f"{ten_file}.txt",
            mime="text/plain"
        )
    else:
        st.info("ℹ️ Chưa có tài liệu nào. Vui lòng tạo kế hoạch hoặc đánh giá trước!")

# ===================== CHÂN TRANG =====================
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: #888; font-size: 14px;'>
    🌸 Ứng dụng hỗ trợ phát hiện sớm & can thiệp sớm — Dựa trên ASQ-3, M-CHAT-R/F, Quyết định 2254/QĐ-BYT & Chương trình Giáo dục Mầm non Việt Nam<br>
    ⚠️ Lưu ý: Ứng dụng là công cụ hỗ trợ, không thay thế đánh giá chuyên môn của bác sĩ, nhà tâm lý, chuyên gia can thiệp sớm
    </p>
""", unsafe_allow_html=True)
