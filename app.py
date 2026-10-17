import streamlit as st
import os
from datetime import datetime
import streamlit as st
from datetime import datetime
import json
from io import BytesIO
# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(
    page_title="Trợ Lý Mầm Non",
    page_icon="🌸",
    layout="wide"
)

# ==================== KHỞI TẠO DỮ LIỆU ====================
if 'danh_sach_tre' not in st.session_state:
    st.session_state.danh_sach_tre = []
if 'tre_hien_tai' not in st.session_state:
    st.session_state.tre_hien_tai = None
if 'lich_su_danh_gia' not in st.session_state:
    st.session_state.lich_su_danh_gia = []

# ==================== DỮ LIỆU CÂU HỎI ASQ-3 ====================
cau_hoi_asq3 = {
    "Giao tiếp": [
        {"cau": "Trẻ có thể chỉ vào đồ vật khi được gọi tên không?", "mo_ta": "Ví dụ: chỉ vào bóng khi người lớn hỏi 'Bóng ở đâu?'"},
        {"cau": "Trẻ có thể nghe và hiểu đơn giản chỉ dẫn không?", "mo_ta": "Ví dụ: 'Đưa cho mẹ cái cốc' mà không cần cử chỉ"},
        {"cau": "Trẻ có thể nói từ đơn có nghĩa không?", "mo_ta": "Ví dụ: mẹ, bố, nước, ăn"},
        {"cau": "Trẻ có thể ghép 2 từ lại với nhau không?", "mo_ta": "Ví dụ: 'Bố đi', 'Uống nước'"},
        {"cau": "Trẻ trả lời khi được hỏi bằng cách nói hay chỉ ra?", "mo_ta": "Không chỉ dùng cử chỉ"},
        {"cau": "Người khác ngoài gia đình có hiểu trẻ nói khoảng một nửa thời gian không?", "mo_ta": "Đối với trẻ 18-36 tháng"}
    ],
    "Vận động tinh": [
        {"cau": "Trẻ có thể nhặt đồ vật nhỏ bằng ngón cái và ngón trỏ không?", "mo_ta": "Không dùng cả nắm tay"},
        {"cau": "Trẻ có thể cầm bút chì/đồ viết và vẽ nguệch ngoạc không?", "mo_ta": "Tự cầm, không cầm giúp"},
        {"cau": "Trẻ có thể lật từng trang sách không?", "mo_ta": "Không lật nhiều trang cùng lúc"},
        {"cau": "Trẻ có thể xếp 2–3 khối gỗ chồng lên nhau không?", "mo_ta": "Tự xếp được"},
        {"cau": "Trẻ có thể vẽ đường thẳng/cong khi được làm mẫu không?", "mo_ta": "Chép theo người lớn"},
        {"cau": "Trẻ có thể cố gắng tự cởi quần áo, tất không?", "mo_ta": "Kéo kéo, cố gắng thực hiện"}
    ],
    "Vận động thô": [
        {"cau": "Trẻ có thể đi một mình không cần nắm tay không?", "mo_ta": "Đi được vài bước đến tự tin đi"},
        {"cau": "Trẻ có thể chạy được không?", "mo_ta": "Chạy dù chưa thật vững"},
        {"cau": "Trẻ có thể nhảy hai chân lên cùng lúc không?", "mo_ta": "Nhảy tại chỗ hoặc bước xuống bậc thang thấp"},
        {"cau": "Trẻ có thể đá bóng khi được chỉ hướng không?", "mo_ta": "Chân tiếp xúc với bóng"},
        {"cau": "Trẻ có thể leo lên ghế/bàn thấp một cách an toàn không?", "mo_ta": "Tự leo lên và xuống cẩn thận"},
        {"cau": "Trẻ có thể đi lên cầu thang với ít hỗ trợ không?", "mo_ta": "Nắm tường/lan can hoặc tự đi"}
    ],
    "Giải quyết vấn đề": [
        {"cau": "Trẻ tìm đồ vật bị che khuất hoàn toàn không?", "mo_ta": "Biết lật khăn/tấm vải ra tìm"},
        {"cau": "Trẻ dùng thử cách khác khi một cách không thành công không?", "mo_ta": "Thay vì khóc, trẻ tìm giải pháp khác"},
        {"cau": "Trẻ bắt chước hành động đơn giản của người lớn không?", "mo_ta": "Làm động tác như quét nhà, lau bàn theo"},
        {"cau": "Trẻ hiểu quan hệ nguyên nhân-kết quả đơn giản không?", "mo_ta": "Biết lắc hộp để nghe tiếng đồ vật bên trong"},
        {"cau": "Trẻ dùng một đồ vật để lấy đồ vật khác không?", "mo_ta": "Dùng que gạt bóng ra xa lại gần hơn"},
        {"cau": "Trẻ có thể phân loại đồ vật theo hình dáng/màu sắc không?", "mo_ta": "Đặt các khối tròn vào chung chỗ"}
    ],
    "Cá nhân - Xã hội": [
        {"cau": "Trẻ có thể tự cầm muỗng ăn được phần nào không?", "mo_ta": "Không cần đút hoàn toàn"},
        {"cau": "Trẻ thể hiện tình cảm với người thân không?", "mo_ta": "Ôm, hôn, mỉm cười khi gặp người thân"},
        {"cau": "Trẻ chơi bên cạnh bạn bè cùng trang lứa không?", "mo_ta": "Chơi song song, quan sát bạn bè"},
        {"cau": "Trẻ bắt chước hành động của bạn bè không?", "mo_ta": "Bạn nhảy thì trẻ cũng nhảy"},
        {"cau": "Trẻ có thể tự rửa tay đơn giản với hướng dẫn không?", "mo_ta": "Cọ xát tay dưới vòi nước"},
        {"cau": "Trẻ chia sẻ đồ vật/đồ ăn khi được nhắc nhở không?", "mo_ta": "Đưa cho người khác dù có thể còn ngần ngại"}
    ]
}

# ==================== THANH BÊN TRÁI ====================
with st.sidebar:
    st.header("👶 Danh sách trẻ")
    
    # ==== HÀM TÍNH THÁNG TUỔI ====
    def tinh_thang_tuoi(ngay_sinh):
        if not ngay_sinh:
            return 0
        hom_nay = datetime.now().date()
        so_thang = (hom_nay.year - ngay_sinh.year) * 12 + (hom_nay.month - ngay_sinh.month)
        if hom_nay.day < ngay_sinh.day:
            so_thang -= 1
        return max(0, so_thang)
    
    def xac_dinh_nhom_tuoi(so_thang):
        if 18 <= so_thang <= 24:
            return "18-24 tháng"
        elif 25 <= so_thang <= 36:
            return "25-36 tháng"
        elif so_thang < 18:
            return f"{so_thang} tháng (dưới 18 tháng)"
        else:
            return f"{so_thang} tháng (trên 36 tháng)"
    
    # ==== THÊM TRẺ MỚI ====
    with st.expander("➕ Thêm trẻ mới"):
        ten_tre_moi = st.text_input("Tên trẻ:")
        ngay_sinh_moi = st.date_input("Ngày sinh:", value=None)
        
        # Tự tính tháng tuổi và nhóm tuổi
        if ngay_sinh_moi:
            thang_tuoi = tinh_thang_tuoi(ngay_sinh_moi)
            nhom_tuoi_tu_dong = xac_dinh_nhom_tuoi(thang_tuoi)
            st.info(f"🎂 **Tháng tuổi hiện tại:** {thang_tuoi} tháng — **Nhóm tuổi:** {nhom_tuoi_tu_dong}")
            
            # Chọn nhóm tuổi (có thể điều chỉnh nếu cần)
            if "18-24" in nhom_tuoi_tu_dong:
                mac_dinh = 0
            elif "25-36" in nhom_tuoi_tu_dong:
                mac_dinh = 1
            else:
                mac_dinh = 0
                st.warning("⚠️ Trẻ ngoài độ tuổi 18-36 tháng — vui lòng chọn nhóm phù hợp nhất!")
            
            nhom_tuoi_moi = st.selectbox("Nhóm độ tuổi:", 
                                           ["18-24 tháng", "25-36 tháng"], 
                                           key="tuoi_moi", index=mac_dinh)
        else:
            nhom_tuoi_moi = st.selectbox("Nhóm độ tuổi:", 
                                           ["18-24 tháng", "25-36 tháng"], 
                                           key="tuoi_moi")
        
        nguoi_danh_gia = st.text_input("Người đánh giá:")
        ghi_chu = st.text_area("Ghi chú:")
        
        if st.button("💾 Lưu trẻ mới"):
            if ten_tre_moi:
                tre_moi = {
                    "id": len(st.session_state.danh_sach_tre) + 1,
                    "ten": ten_tre_moi,
                    "ngay_sinh": ngay_sinh_moi,
                    "tuoi": nhom_tuoi_moi,
                    "nguoi_danh_gia": nguoi_danh_gia,
                    "ngay_tao": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "ghi_chu": ghi_chu
                }
                st.session_state.danh_sach_tre.append(tre_moi)
                st.success(f"✅ Đã thêm: {ten_tre_moi}")
                st.rerun()
            else:
                st.warning("⚠️ Nhập tên trẻ trước khi lưu!")
    
    # ==== CHỌN TRẺ ĐỂ LÀM VIỆC ====
    st.subheader("📋 Chọn trẻ đã lưu")
    if st.session_state.danh_sach_tre:
        danh_sach_ten = [f"{t['ten']} ({t['tuoi']})" for t in st.session_state.danh_sach_tre]
        chi_so_chon = st.selectbox("Chọn trẻ cần đánh giá:", 
                                    range(len(danh_sach_ten)), 
                                    format_func=lambda i: danh_sach_ten[i])
        st.session_state.tre_hien_tai = st.session_state.danh_sach_tre[chi_so_chon]
        tre = st.session_state.tre_hien_tai
        
    # Tính tháng tuổi hiển thị
        if 'ngay_sinh' in tre and tre['ngay_sinh']:
            try:
                from datetime import datetime
                ns = tre['ngay_sinh']
                if isinstance(ns, datetime):
                    ns_date = ns.date()
                else:
                    ns_date = ns
                
                hom_nay = datetime.now().date()
                thang_tuoi = (hom_nay.year - ns_date.year) * 12 + (hom_nay.month - ns_date.month)
                if hom_nay.day < ns_date.day:
                    thang_tuoi -= 1
                thang_tuoi = max(0, thang_tuoi)
                
                st.info(f"✅ Đang làm việc với: **{tre['ten']}** — {thang_tuoi} tháng tuổi")
            except:
                st.info(f"✅ Đang làm việc với: **{tre['ten']}**")
        else:
            st.info(f"✅ Đang làm việc với: **{tre['ten']}**")
        
        # Nút xóa trẻ
        if st.button("🗑️ Xóa trẻ này"):
            st.session_state.danh_sach_tre.pop(chi_so_chon)
            if st.session_state.danh_sach_tre:
                st.session_state.tre_hien_tai = st.session_state.danh_sach_tre[0]
            else:
                st.session_state.tre_hien_tai = None
            st.success("✅ Đã xóa!")
            st.rerun()
    else:
        st.info("Chưa có trẻ nào. Nhấn 'Thêm trẻ mới' ở trên nhé!")
    
    st.divider()
    st.subheader("📋 Chức năng chính")
    tab_chon = st.radio("Chọn chức năng:", [
        "📝 Đánh giá phát triển ASQ-3",
        "🔍 Sàng lọc sớm",
        "📄 Tạo kế hoạch cá nhân",
        "🎮 Tài nguyên trò chơi",
        "📊 Lịch sử đánh giá"
    ])

# ==================== TIÊU ĐỀ CHÍNH ====================
st.markdown("""
# 🌸 Hỗ Trợ Trẻ Mầm Non - Phát Hiện & Can Thiệp Sớm
> **Công cụ dành cho giáo viên và phụ huynh** — Đánh giá theo bộ công cụ ASQ-3
""")
st.divider()

# ==================== TAB 1: ĐÁNH GIÁ ASQ-3 ====================
if tab_chon == "📝 Đánh giá phát triển ASQ-3":
    if not st.session_state.tre_hien_tai:
        st.info("👈 Vui lòng nhập thông tin trẻ ở thanh bên trái trước khi đánh giá!")
    else:
        tre = st.session_state.tre_hien_tai
        ten_tre = tre.get('ten', 'Không có tên')
        tuoi_tre = tre.get('tuoi', 'Không rõ độ tuổi')
        ngay_dg = tre.get('ngay_danh_gia', tre.get('ngay_tao', datetime.now().strftime("%d/%m/%Y %H:%M")))
        nguoi_dg = tre.get('nguoi_danh_gia', tre.get('nguoi_danh_gia', 'Chưa ghi'))
        
        st.subheader(f"📋 Đánh giá ASQ-3 cho: {ten_tre} — {tuoi_tre}")
        st.caption(f"Ngày: {ngay_dg} | Người đánh giá: {nguoi_dg}")
        st.caption("Trả lời dựa trên quan sát thực tế của trẻ trong 1-2 tháng qua:")
        
        tong_diem = {}
        for linh_vuc, danh_sach_cau in cau_hoi_asq3.items():
            st.markdown(f"### ✅ {linh_vuc} (6 câu)")
            st.caption("Trả lời dựa trên quan sát thực tế của trẻ trong 1-2 tháng qua:")
            
            diem_linh_vuc = 0
            for so_thu_tu, cau_hoi in enumerate(danh_sach_cau, 1):
                st.markdown(f"**Câu {so_thu_tu}/6:** {cau_hoi['cau']}")
                st.caption(f"💡 {cau_hoi['mo_ta']}")
                
                lua_chon = st.radio(
                    label=f"Đáp án {so_thu_tu}",
                    options=["Có", "Đôi khi", "Chưa"],
                    key=f"asq3_{linh_vuc}_{so_thu_tu}",
                    index=2,
                    horizontal=True
                )
                
                if lua_chon == "Có":
                    diem_linh_vuc += 10
                elif lua_chon == "Đôi khi":
                    diem_linh_vuc += 5
                else:
                    diem_linh_vuc += 0
                st.divider()
            
            tong_diem[linh_vuc] = diem_linh_vuc
            st.info(f"📊 **Tổng điểm: {diem_linh_vuc}/60**")
            st.progress(diem_linh_vuc / 60)
            
            if diem_linh_vuc >= 50:
                st.success("✅ Phát triển tốt — tiếp tục duy trì môi trường hỗ trợ!")
            elif 30 <= diem_linh_vuc < 50:
                st.warning("⚠️ Cần chú ý hỗ trợ thêm — xem Kế hoạch cá nhân để có giải pháp cụ thể.")
            else:
                st.error("🔴 Khuyến nghị sàng lọc thêm & xây dựng kế hoạch can thiệp chuyên sâu!")
            st.markdown("---")
        
        if st.button("💾 Lưu kết quả đánh giá"):
            ket_qua = {
                "ten_tre": ten_tre,
                "tuoi": tuoi_tre,
                "ngay": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "nguoi_danh_gia": nguoi_dg,
                "diem": tong_diem,
                "ghi_chu": tre.get('ghi_chu', '')
            }
            st.session_state.lich_su_danh_gia.append(ket_qua)
            st.success("🎉 Đã lưu! Chuyển tab 'Kế hoạch cá nhân' để xây dựng giải pháp hỗ trợ nhé!")
        # Nút xem lịch sử nhanh
        st.markdown("---")
        if st.button("📊 Xem tất cả hồ sơ đã lưu"):
            st.info("👉 Chuyển tab 'Lịch sử đánh giá' để xem chi tiết tất cả hồ sơ nhé!")
# ==================== TAB 2: SÀNG LỌC SỚM ====================
# ==================== TAB 2: SÀNG LỌC SỚM ====================
elif tab_chon == "🔍 Sàng lọc sớm":
    st.subheader("🔍 Bảng sàng lọc dấu hiệu phát triển trẻ mầm non")
    # === Hiển thị thông tin trẻ đang được chọn ===
if 'tre_hien_tai' in st.session_state and st.session_state.tre_hien_tai:
    tre = st.session_state.tre_hien_tai
    st.info(f"""
    👶 **Đang sàng lọc cho:** {tre.get('ten', 'Chưa có tên')}
    📅 **Ngày sinh:** {tre.get('ngay_sinh', 'Chưa có thông tin')}
    🎂 **Độ tuổi:** {tre.get('tuoi', 'Chưa xác định')}
    """)
    
    # Tự động chọn nhóm tuổi phù hợp với trẻ
    tuoi_tre = tre.get('tuoi', '')
    nhom_tuoi_mapping = {
        '18-24 tháng': '18-24 tháng',
        '25-36 tháng': '25-36 tháng',
        '37-48 tháng': '37-48 tháng',
        '49-60 tháng': '49-60 tháng',
        '61-72 tháng': '61-72 tháng'
    }
    nhom_tuoi_mac_dinh = nhom_tuoi_mapping.get(tuoi_tre, '25-36 tháng')
else:
    nhom_tuoi_mac_dinh = '25-36 tháng'
    st.warning("⚠️ Vui lòng chọn trẻ từ danh sách bên trái để sàng lọc chính xác hơn!")

# Chọn nhóm độ tuổi cần sàng lọc
nhom_tuoi_sang_loc = st.selectbox(
    "Chọn nhóm độ tuổi cần sàng lọc:",
    ['18-24 tháng', '25-36 tháng', '37-48 tháng', '49-60 tháng', '61-72 tháng'],
    index=['18-24 tháng', '25-36 tháng', '37-48 tháng', '49-60 tháng', '61-72 tháng'].index(nhom_tuoi_mac_dinh)
)
st.info("Danh mục các dấu hiệu cần quan sát — Phát hiện sớm những khó khăn có thể có của trẻ")
 else:
    nhom_tuoi_mac_dinh = '25-36 tháng'
    st.warning("⚠️ Vui lòng chọn trẻ từ danh sách bên trái để sàng lọc chính xác hơn!")

# Chọn nhóm độ tuổi cần sàng lọc
danh_sach_nhom_tuoi = ['18-24 tháng', '25-36 tháng', '37-48 tháng', '49-60 tháng', '61-72 tháng']
vi_tri_mac_dinh = danh_sach_nhom_tuoi.index(nhom_tuoi_mac_dinh) if nhom_tuoi_mac_dinh in danh_sach_nhom_tuoi else 1

nhom_tuoi_sang_loc = st.selectbox(
    "Chọn nhóm độ tuổi cần sàng lọc:",
    danh_sach_nhom_tuoi,
    index=vi_tri_mac_dinh
)
st.info("Danh mục các dấu hiệu cần quan sát — Phát hiện sớm những khó khăn có thể có của trẻ")
st.markdown("---")

# Dữ liệu sàng lọc theo độ tuổi
if nhom_tuoi_sang_loc == "18-24 tháng":
    du_lieu_sang_loc = {
        "Ngôn ngữ & Giao tiếp": [
            ("Trẻ có thể chỉ ra đồ vật khi được gọi tên?", False),
            ("Trẻ có thể nói ít nhất 6-10 từ có nghĩa?", False),
            ("Trẻ có thể nói yêu cầu đơn giản không cần chỉ?", False)
        ]
    }
    st.markdown("---")
    # Dữ liệu dấu hiệu sàng lọc theo độ tuổi
    if nhom_tuoi_sang_loc == "18–24 tháng":
        du_lieu_sang_loc = {
            "Ngôn ngữ & Giao tiếp": [
                ("Trẻ có thể chỉ ra đồ vật khi được gọi tên?", False),
                ("Trẻ có thể nói ít nhất 6–10 từ có nghĩa?", False),
                ("Trẻ có thể làm theo yêu cầu đơn giản không cần cử chỉ?", False),
                ("Trẻ có thể thu hút sự chú ý của người khác khi cần giúp đỡ?", False)
            ],
            "Vận động": [
                ("Trẻ có thể đi độc lập, không cần nắm tay?", False),
                ("Trẻ có thể nhặt đồ vật nhỏ bằng ngón tay cái và ngón trỏ?", False),
                ("Trẻ có thể gõ hai vật vào nhau?", False),
                ("Trẻ có thể lật từng trang sách?", False)
            ],
            "Xã hội & Cảm xúc": [
                ("Trẻ có thể bắt chước hành động đơn giản của người lớn?", False),
                ("Trẻ quan tâm đến trẻ khác, nhìn hoặc đến gần bạn cùng trang lứa?", False),
                ("Trẻ có thể biểu lộ cảm xúc rõ ràng khi vui hoặc không vui?", False),
                ("Trẻ phản hồi khi được gọi tên?", False)
            ],
            "Hành vi & Chú ý": [
                ("Trẻ có thể duy trì chú ý với một hoạt động ít nhất 2–3 phút?", False),
                ("Trẻ có thể chơi với đồ vật theo chức năng (không chỉ cầm ném)?", False),
                ("Trẻ tiếp xúc bằng mắt khi tương tác?", False),
                ("Trẻ không có hành vi lặp đi lặp lại bất thường (vẫy tay, lắc đầu liên tục)?", False)
            ]
        }
    else: # 25–36 tháng
        du_lieu_sang_loc = {
            "Ngôn ngữ & Giao tiếp": [
                ("Trẻ có thể nói cụm từ gồm 2–3 từ?", False),
                ("Trẻ trả lời câu hỏi đơn giản bằng lời nói?", False),
                ("Người ngoài gia đình hiểu được khoảng 50% lời nói của trẻ?", False),
                ("Trẻ kể lại một sự việc đơn giản đã xảy ra?", False)
            ],
            "Vận động": [
                ("Trẻ có thể chạy, dừng lại và đổi hướng?", False),
                ("Trẻ có thể đá bóng về phía trước?", False),
                ("Trẻ có thể xếp 4–6 khối gỗ chồng lên nhau?", False),
                ("Trẻ cố gắng tự cởi quần áo, tất dép?", False)
            ],
            "Xã hội & Cảm xúc": [
                ("Trẻ chơi cùng bạn bè, chia sẻ đồ vật đơn giản?", False),
                ("Trẻ có thể thực hiện theo quy tắc đơn giản?", False),
                ("Trẻ thể hiện sự đồng cảm khi người khác buồn?", False),
                ("Trẻ tách khỏi người thân mà không quá hoảng sợ?", False)
            ],
            "Hành vi & Chú ý": [
                ("Trẻ có thể hoàn thành một nhiệm vụ đơn giản theo hướng dẫn?", False),
                ("Trẻ không có hành vi tự gây đau cho bản thân?", False),
                ("Trẻ đa dạng hóa cách chơi với đồ vật khác nhau?", False),
                ("Trẻ đáp ứng với tên gọi của mình một cách nhất quán?", False)
            ]
        }
    
    # Lưu trạng thái trả lời
    ket_qua_sang_loc = {}
    tong_dau_hieu = 0
    tong_dau_hieu_chua_dat = 0
    
    for nhom, danh_sach_dau_hieu in du_lieu_sang_loc.items():
        st.markdown(f"### 📌 {nhom}")
        st.caption(f"Đánh dấu ✅ nếu trẻ thể hiện được dấu hiệu này")
        
        for i, (dau_hieu, mac_dinh) in enumerate(danh_sach_dau_hieu):
            da_dat = st.checkbox(dau_hieu, value=mac_dinh, key=f"sl_{nhom}_{i}")
            ket_qua_sang_loc[f"{nhom} - {dau_hieu}"] = da_dat
            tong_dau_hieu += 1
            if not da_dat:
                tong_dau_hieu_chua_dat += 1
        
        st.markdown("---")
    
    # Nút xem kết quả
    if st.button("📊 Xem kết quả sàng lọc"):
        ty_le_chua_dat = tong_dau_hieu_chua_dat / tong_dau_hieu * 100
        ty_le_dat = 100 - ty_le_chua_dat
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tổng số dấu hiệu", tong_dau_hieu)
        with col2:
            st.metric("Số dấu hiệu chưa thể hiện", tong_dau_hieu_chua_dat)
        
        st.progress(ty_le_dat / 100)
        
        # Đánh giá và khuyến nghị
        if ty_le_chua_dat >= 40:
            st.error("""
### 🔴 Cần chú ý — Khuyến nghị tham khảo chuyên gia
- Nhiều dấu hiệu phát triển chưa thể hiện rõ
- **Khuyến nghị:** Thực hiện đánh giá chi tiết hơn bằng bộ ASQ-3 và tham khảo ý kiến chuyên gia tâm lý/trị liệu ngôn ngữ
- Quan sát và ghi chép thêm hành vi của trẻ trong sinh hoạt hàng ngày
            """)
        elif 20 <= ty_le_chua_dat < 40:
            st.warning("""
### ⚠️ Cần theo dõi và hỗ trợ thêm
- Một số dấu hiệu chưa thể hiện rõ hoặc chưa ổn định
- **Khuyến nghị:** Tạo điều kiện và môi trường hỗ trợ trẻ thực hiện các kỹ năng này thông qua trò chơi hàng ngày
- Theo dõi lại sau 1–2 tháng
            """)
        else:
            st.success("""
### ✅ Phát triển theo lộ trình bình thường
- Hầu hết các dấu hiệu quan sát được đều thể hiện tốt
- **Khuyến nghị:** Tiếp tục duy trì môi trường yêu thương, kích thích phát triển toàn diện cho trẻ
            """)
    
    # Lưu kết quả
    if st.button("💾 Lưu kết quả sàng lọc"):
        st.session_state.lich_su_danh_gia.append({
            "ngay": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "loai_danh_gia": "Sàng lọc sớm",
            "nhom_tuoi": nhom_tuoi_sang_loc,
            "dau_hieu_tong": tong_dau_hieu,
            "dau_hieu_chua_dat": tong_dau_hieu_chua_dat,
            "chi_tiet": ket_qua_sang_loc
        })
        st.success("✅ Đã lưu kết quả sàng lọc vào lịch sử!")
        # Liên kết xem hồ sơ
        st.markdown("---")
        st.info("💡 Để xem lại các lần sàng lọc trước, chuyển sang tab **'📊 Lịch sử đánh giá'** ở thanh bên trái!")
# ==================== TAB 3: KẾ HOẠCH CÁ NHÂN ====================
# ==================== TAB 3: KẾ HOẠCH CÁ NHÂN VỚI AI ====================
elif tab_chon == "📄 Tạo kế hoạch cá nhân":
    st.subheader("🤖 AI Trợ lý — Tạo Kế hoạch Hỗ trợ Cá nhân")
    
    if not st.session_state.tre_hien_tai:
        st.warning("⚠️ Vui lòng chọn trẻ ở thanh bên trái trước khi tạo kế hoạch!")
    else:
        tre = st.session_state.tre_hien_tai
        ten_tre = tre.get('ten', 'Trẻ')
        tuoi_tre = tre.get('tuoi', '')
        ngay_sinh = tre.get('ngay_sinh', '')
        nguoi_lap = st.text_input("Người lập kế hoạch:", value=tre.get('nguoi_danh_gia', ''))
        ngay_lap = datetime.now().strftime("%d/%m/%Y")
        
        st.info(f"📋 Đang lập kế hoạch cho: **{ten_tre}** — {tuoi_tre}")
        st.divider()
        
        # ==== Bước 1: Xác định thông tin & khó khăn ====
        st.markdown("### 🔍 Bước 1: Thông tin phân tích")
        
        diem_manh = st.text_area("💪 Điểm mạnh của trẻ:",
            placeholder="Ví dụ: Trẻ rất thân thiện, thích nghe truyện, nhớ nhanh bài hát...", height=80)
        
        linh_vuc_can_ho_tro = st.multiselect("📌 Lĩnh vực cần ưu tiên hỗ trợ:",
            ["Ngôn ngữ & Giao tiếp", "Vận động tinh", "Vận động thô", 
             "Giải quyết vấn đề", "Kỹ năng xã hội", "Tự phục vụ", "Chú ý & Hành vi"])
        
        muc_do = st.radio("📊 Mức độ cần hỗ trợ theo ASQ-3:",
            ["🔵 Phát triển bình thường — theo dõi định kỳ",
             "🟡 Cần hỗ trợ thêm tại nhà & lớp",
             "🔴 Khuyến nghị can thiệp có hướng dẫn chuyên gia"],
            index=1)
        
        mo_ta_kho_khan = st.text_area("📝 Mô tả cụ thể khó khăn & hành vi quan sát được:",
            placeholder="Mô tả những gì trẻ chưa làm được, tình huống khó khăn xuất hiện như thế nào, tần suất...", height=120)
        
        st.divider()
        
        # ==== Bước 2: AI TẠO KẾ HOẠCH TỰ ĐỘNG ====
        st.markdown("### 🤖 Bước 2: AI Tạo gợi ý kế hoạch chi tiết")
        
        # Dữ liệu gợi ý chuẩn theo ASQ-3 và Can thiệp sớm
        goi_y_chuan = {
            "Ngôn ngữ & Giao tiếp": {
                "muc_tieu_ngan_han": "Trẻ hiểu và thực hiện được 2 chỉ dẫn nối tiếp; Gọi được tên 5–10 đồ vật quen thuộc; Từ vựng tăng 3–5 từ mới mỗi tuần",
                "muc_tieu_dai_han": "Trẻ giao tiếp được nhu cầu cơ bản bằng cụm từ/câu đơn giản; Hiểu và trả lời được câu hỏi đơn giản (ai, cái gì, ở đâu)",
                "hoat_dong": """**🔹 Hoạt động hàng ngày:**
- Đọc sách ảnh cùng trẻ 10–15 phút/ngày — đặt câu hỏi, chỉ và gọi tên hình ảnh
- Mô tả hành động đang làm: 'Mẹ đang rửa tay', 'Con đang cầm cốc'
- Hát bài hát có lời đơn giản, lặp lại nhiều lần
- Chơi trò chơi 'Đồ vật gì đang thiếu?' — che 1 đồ vật, hỏi trẻ cái gì mất đi

🔹 Hoạt động tại lớp:
- Nhóm đọc truyện theo chủ đề quen thuộc
- Trẻ đóng vai nhân vật trong truyện
- Trò chơi nghe lệnh: 'Lấy quả bóng đỏ', 'Đặt sách lên bàn'

🔹 Tại nhà:
- Thường xuyên nói chuyện, bình luận hành động của trẻ — không dùng TV/điện thoại thay giao tiếp trực tiếp
- Khuyến khích trẻ chỉ và gọi tên đồ vật thay vì chỉ dùng cử chỉ""",
                "tan_suat": "Hàng ngày, 10–15 phút mỗi lần",
                "ghi_chu": "Kiên nhẫn, khen ngợi mọi nỗ lực giao tiếp của trẻ. Không sửa lỗi trực tiếp mà nhắc lại đúng mẫu."
            },
            "Vận động tinh": {
                "muc_tieu_ngan_han": "Nhặt đồ vật nhỏ bằng ngón cái-trỏ; Xếp được 3–5 khối chồng lên nhau; Lật được từng trang sách",
                "muc_tieu_dai_han": "Vẽ được nét thẳng/tròn theo mẫu; Cầm muỗng ăn ít rớt hơn; Cởi được tất, kéo khóa đơn giản",
                "hoat_dong": """**🔹 Hoạt động hàng ngày:**
- Nhặt hạt/đồ vật nhỏ bỏ vào hộp — quan sát dùng ngón cái-trỏ
- Xếp tháp khối gỗ, cốc nhựa
- Vẽ nguệch ngoạc, tô màu trong khung đơn giản
- Xé giấy, vo giấy thành quả bóng
- Chơi với đất nặn/bột màu: ấn, nhào, nặn hình đơn giản

🔹 Hoạt động tại lớp:
- Trò chơi chuỗi hạt lớn
- Xếp hình ghép đơn giản (2–4 mảnh)
- Tô màu hình lớn viền đậm
- Cắt giấy an toàn với kéo nhựa

🔹 Tại nhà:
- Khuyến khích tự cầm muỗng, tự cầm cốc uống nước
- Tự cố gắng cởi giày, tất, nắp hộp nhựa""",
                "tan_suat": "2–3 lần/ngày, 5–10 phút mỗi lần",
                "ghi_chu": "Không đòi hỏi sự hoàn hảo — tập trung vào sự cố gắng và niềm vui thực hiện."
            },
            "Vận động thô": {
                "muc_tieu_ngan_han": "Đi/chạy tự tin hơn; Ném bóng về phía mục tiêu; Đứng trên 1 chân 2–3 giây",
                "muc_tieu_dai_han": "Nhảy 2 chân tại chỗ; Đi lên/xuống cầu thang không cần nắm tay; Đạp xe 3 bánh",
                "hoat_dong": """**🔹 Hoạt động hàng ngày:**
- Đi bộ trên bề mặt khác nhau: cỏ, gỗ, sàn nhà
- Chơi ném-bắt bóng lớn
- Nhảy qua vạch kẻ trên sàn
- Đi theo đường thẳng vẽ trên đất
- Leo lên/xuống ghế thấp an toàn

🔹 Hoạt động ngoài trời:
- Chạy theo bạn bè, trò chơi đuổi bắt đơn giản
- Đạp xe 3 bánh
- Nhảy lò cò đơn giản
- Vượt chướng ngại vật thấp

🔹 Tại nhà:
- Khuyến khích trẻ tự di chuyển thay vì bế
- Tạo không gian an toàn để trẻ tự do vận động""",
                "tan_suat": "Hàng ngày, 20–30 phút ngoài trời",
                "ghi_chu": "An toàn trên hết — quan sát và hỗ trợ khi cần, không can thiệp quá nhiều."
            },
            "Giải quyết vấn đề": {
                "muc_tieu_ngan_han": "Tìm được đồ vật bị che hoàn toàn; Thử cách khác khi cách 1 không thành công; Bắt chước hành động đơn giản",
                "muc_tieu_dai_han": "Phân loại đồ vật theo màu/hình dạng; Sử dụng đồ vật làm công cụ đơn giản; Hoàn thành được chuỗi hành động đơn giản",
                "hoat_dong": """**🔹 Hoạt động nhận thức:**
- Trò chơi 'Đồ vật biến mất' — che khăn, hỏi trẻ tìm
- Đóng hộp có nắp khác nhau — trẻ tự tìm cách mở
- Phân loại đồ vật theo màu, kích thước, hình dạng
- Xếp chuỗi vòng tròn/khối theo kích thước giảm dần

🔹 Trò chơi nguyên nhân-kết quả:
- Lắc hộp có đồ vật bên trong để nghe tiếng
- Đẩy xe lăn xem nó di chuyển như thế nào
- Thả đồ vật vào nước — nổi hay chìm?

🔹 Tư duy linh hoạt:
- Khi trẻ gặp khó khăn, chờ 5–10 giây trước khi giúp
- Hướng dẫn trẻ thử cách khác thay vì làm giúp""",
                "tan_suat": "2–3 lần/tuần, 10–15 phút",
                "ghi_chu": "Đặt câu hỏi gợi mở: 'Làm sao để lấy ra nhỉ?' thay vì trực tiếp làm giúp."
            },
            "Kỹ năng xã hội": {
                "muc_tieu_ngan_han": "Chơi bên cạnh bạn 5–10 phút; Chia sẻ đồ vật khi được nhắc nhở; Giao tiếp bằng mắt khi tương tác",
                "muc_tieu_dai_han": "Chơi cùng bạn theo quy tắc đơn giản; Thể hiện sự quan tâm khi bạn buồn; Tự giới thiệu tên khi được hỏi",
                "hoat_dong": """**🔹 Hoạt động nhóm:**
- Chơi song song cùng bạn với đồ vật giống nhau
- Trò chơi lặp vòng: đưa đồ vật cho bạn bên cạnh
- Bắt chước hành động bạn bè: vỗ tay, nhảy, cười
- Hát múa theo nhạc cùng nhóm

🔹 Học chia sẻ & quan tâm:
- Dạy trẻ đưa đồ chơi cho bạn rồi nhận lại
- Chỉ vào bạn và nói: 'Bạn đang buồn, ôm bạn nhé'
- Chào hỏi khi đến lớp, tạm biệt khi về nhà

🔹 Tự phục vụ & độc lập:
- Tự cởi/đeo dép, mũ
- Rửa tay, lau mặt theo hướng dẫn
- Ăn cơm tự lập hơn""",
                "tan_suat": "Hàng ngày trong mọi hoạt động sinh hoạt",
                "ghi_chu": "Khen ngợi ngay khi trẻ có hành vi tích cực. Không phê bình khi trẻ chưa làm được — lặp lại hướng dẫn."
            },
            "Tự phục vụ": {
                "muc_tieu_ngan_han": "Tự cầm muỗng ăn; Tự cởi tất/dép; Rửa tay với hướng dẫn",
                "muc_tieu_dai_han": "Tự ăn không cần giúp nhiều; Tự mặc quần áo đơn giản; Biết tự đi vệ sinh",
                "hoat_dong": """**🔹 Ăn uống:**
- Để trẻ tự cầm muỗng dù có rớt thức ăn
- Cắt thức ăn nhỏ, dễ xúc
- Dùng bát đĩa không vỡ, có đáy chống trượt

🔹 Vệ sinh cá nhân:
- Tự rửa tay theo 4 bước đơn giản: làm ướt → xà phòng → rửa sạch → lau khô
- Tự kéo quần lên/xuống khi đi vệ sinh
- Tự lau mặt bằng khăn mềm

🔹 Quần áo:
- Tự cố gắng đưa tay vào tay áo, chân vào quần
- Tự cởi khóa dán dép, mũ, nón""",
                "tan_suat": "Tạo cơ hội tự làm mọi lúc trong ngày",
                "ghi_chu": "Kiên nhẫn — trẻ cần thời gian. Hãy chậm lại và cho trẻ thực hiện theo tốc độ của mình."
            },
            "Chú ý & Hành vi": {
                "muc_tieu_ngan_han": "Duy trì chú ý 3–5 phút với hoạt động yêu thích; Chuyển hoạt động mà không quá cáu giận; Giảm hành vi lặp lại bất thường",
                "muc_tieu_dai_han": "Chú ý 5–10 phút với hoạt động có hướng dẫn; Thể hiện cảm xúc phù hợp hơn; Hạn chế hành vi tự gây tổn thương",
                "hoat_dong": """**🔹 Rèn khả năng tập trung:**
- Bắt đầu với hoạt động trẻ yêu thích, thời gian ngắn rồi tăng dần
- Loại bỏ yếu tố gây xao nhãng khi trẻ đang làm việc
- Trò chơi 'Đừng làm động tác này' — rèn tự điều chỉnh
- Nghe nhạc nhẹ khi cần bình tĩnh

🔹 Quản lý cảm xúc & chuyển tiếp:
- Thông báo trước khi thay đổi hoạt động: 'Còn 5 phút nữa chúng ta dừng lại nhé'
- Sử dụng tín hiệu hình ảnh/đồng hồ trực quan để trẻ chuẩn bị
- Dạy trẻ cách bình tĩnh: thở sâu, đếm từ 1–5 khi tức giận

🔹 Hành vi tích cực:
- Dùng biểu đồ nhãn dán: mỗi lần trẻ chơi yên 5 phút → dán 1 ngôi sao
- Khen ngợi hành vi mong muốn ngay khi xuất hiện: 'Con ngồi yên nghe cô nói thật tốt!'""",
                "tan_suat": "Luyện tập hàng ngày, nhất là trong các chuyển tiếp hoạt động",
                "ghi_chu": "Tính nhất quán là quan trọng nhất. Cùng một quy tắc giữa nhà và trường."
            }
        }
        
        # Nút tạo kế hoạch AI
        if st.button("🤖 AI TẠO KẾ HOẠCH CHI TIẾT", type="primary"):
            if not linh_vuc_can_ho_tro:
                st.error("⚠️ Vui lòng chọn ít nhất 1 lĩnh vực cần hỗ trợ trước!")
            else:
                st.success("✅ AI đang phân tích & tạo kế hoạch...")
                st.balloons()
                
                st.markdown("---")
                st.markdown(f"""
                # 📋 KẾ HOẠCH HỖ TRỢ PHÁT TRIỂN CÁ NHÂN
                **Tên trẻ:** {ten_tre}  |  **Ngày sinh:** {ngay_sinh}
                **Nhóm độ tuổi:** {tuoi_tre}  |  **Ngày lập:** {ngay_lap}
                **Người lập:** {nguoi_lap}
                
                ---
                
                ## 💪 I. Thông tin chung & Điểm mạnh
                **Điểm mạnh của trẻ:**
                {diem_manh or '*Chưa ghi nhận — quan sát thêm trong sinh hoạt hàng ngày*'}
                
                **Mức độ hỗ trợ:**
                > {muc_do}
                
                **Khó khăn chính:**
                {mo_ta_kho_khan or '*Chưa mô tả chi tiết — tiếp tục quan sát và cập nhật*'}
                
                ---
                
                ## 🎯 II. Mục tiêu hỗ trợ chính
                """)
                
                # Tạo kế hoạch cho từng lĩnh vực được chọn
                tong_muc_tieu_ngan_han = []
                tong_muc_tieu_dai_han = []
                tong_giai_phap = []
                
                for lv in linh_vuc_can_ho_tro:
                    if lv in goi_y_chuan:
                        du_lieu = goi_y_chuan[lv]
                        
                        tong_muc_tieu_ngan_han.append(f"**{lv}:** {du_lieu['muc_tieu_ngan_han']}")
                        tong_muc_tieu_dai_han.append(f"**{lv}:** {du_lieu['muc_tieu_dai_han']}")
                        
                        tong_giai_phap.append(f"""
                        ### 📌 {lv}
                        
                        **🎯 Mục tiêu ngắn hạn (1–3 tháng):**
                        {du_lieu['muc_tieu_ngan_han']}
                        
                        **🎯 Mục tiêu dài hạn (6–12 tháng):**
                        {du_lieu['muc_tieu_dai_han']}
                        
                        **🛠️ Hoạt động cụ thể:**
                        {du_lieu['hoat_dong']}
                        
                        **⏰ Tần suất:** {du_lieu['tan_suat']}
                        
                        **💡 Lưu ý quan trọng:**
                        {du_lieu['ghi_chu']}
                        
                        ---
                        """)
                
                # Hiển thị mục tiêu tổng hợp
                st.markdown("### 📋 Mục tiêu tổng hợp theo từng lĩnh vực")
                with st.expander("Xem tóm tắt mục tiêu"):
                    st.markdown("#### Mục tiêu ngắn hạn:")
                    for mt in tong_muc_tieu_ngan_han:
                        st.markdown(f"- {mt}")
                    st.markdown("#### Mục tiêu dài hạn:")
                    for mt in tong_muc_tieu_dai_han:
                        st.markdown(f"- {mt}")
                
                # Hiển thị kế hoạch chi tiết
                st.markdown("---")
                st.markdown("## 📖 III. KẾ HOẠCH CHI TIẾT THEO LĨNH VỰC")
                
                for gp in tong_giai_phap:
                    with st.expander(f"📌 Xem chi tiết hoạt động — {gp.split('### 📌 ')[1].split(chr(10))[0]}"):
                        st.markdown(gp)
                
                # Phần phối hợp & theo dõi
                st.markdown("---")
                st.markdown("""
                ## 🤝 IV. Phối hợp giữa Gia đình & Trường
                
                **✅ Nguyên tắc chung:**
                - Tính nhất quán giữa nhà và trường là yếu tố quan trọng nhất
                - Thông tin trao đổi thường xuyên qua sổ liên lạc/nhóm Zalo
                - Quan sát và ghi chép tiến độ mỗi tuần
                - Điều chỉnh kế hoạch linh hoạt theo sự phát triển của trẻ
                
                **📅 Chu kỳ xem xét lại kế hoạch:**
                - Rà soát hàng tháng: điều chỉnh hoạt động, tần suất phù hợp
                - Đánh giá tổng thể sau 3–6 tháng: xem xét lại mục tiêu dài hạn
                - Tham khảo chuyên gia nếu sau 6 tháng không có tiến triển rõ rệt
                
                **📝 Ghi chú:**
                - Đây là kế hoạch tham khảo dựa trên tài liệu ASQ-3 và hướng dẫn Can thiệp sớm Việt Nam
                - Mỗi trẻ có tốc độ phát triển riêng — điều chỉnh theo thực tế của con
                - Khi có dấu hiệu cần hỗ trợ chuyên sâu hơn, vui lòng tham khảo chuyên gia tâm lý/trị liệu ngôn ngữ/phát triển trẻ
                """)
                
                st.markdown("---")
                st.info("""
                📄 **Bạn có thể:**
                - In toàn bộ nội dung trên để lưu vào hồ sơ trẻ
                - Tùy chỉnh, bổ sung hoạt động cho phù hợp với điều kiện thực tế
                - Lưu bản sao vào tab 'Lịch sử đánh giá' để theo dõi tiến độ
                """)
        
        st.divider()
        
        # Nút lưu kế hoạch do người dùng tự điền
        st.markdown("### 💾 Lưu kế hoạch tự chỉnh sửa")
        # ==== NÚT TẢI KẾ HOẠCH RA TỆP WORD ====
        st.subheader("📄 Tải kế hoạch ra tệp Word")

        noi_dung_word = f"""
        KE HOACH HO TRO PHAT TRIEN CA NHAN
        ====================================
        
        Ten tre: {ten_tre}
        Ngay sinh: {ngay_sinh}
        Nhom do tuoi: {tuoi_tre}
        Ngay lap: {datetime.now().strftime('%d/%m/%Y')}
        Nguoi lap: {nguoi_lap}
        
        === I. DIEM MANH CUA TRE ===
        {diem_manh or 'Chua ghi nhan'}

        === II. LINH VUC CAN HO TRO ===
        {', '.join(linh_vuc_can_ho_tro) if linh_vuc_can_ho_tro else 'Chua chon linh vuc'}
        
        Muc do ho tro: {muc_do}
        """
        
        if 'mo_ta_kho_khan' in locals():
            noi_dung_word += f"\nMo ta kho khan:\n{mo_ta_kho_khan}\n"
        
        noi_dung_word += f"""
        === III. MUU TIEU HO TRO ===
        Muc tieu ngan han (1-3 thang):
        {muc_tieu_ngan_han if 'muc_tieu_ngan_han' in locals() else 'Chua dat muc tieu'}
        
        Muc tieu dai han (6-12 thang):
        {muc_tieu_dai_han if 'muc_tieu_dai_han' in locals() else 'Chua dat muc tieu'}
        """
        
        if 'giai_phap' in locals() and giai_phap:
            noi_dung_word += "\n=== IV. GIAI PHAP HOAT DONG ===\n"
            for lv, thong_tin in giai_phap.items():
                noi_dung_word += f"""
        ---
        {lv.upper()}:
        - Hoat dong: {thong_tin.get('hoat_dong', 'Chua mo ta')}
        - Tan suat: {thong_tin.get('tan_suat', 'Chua ghi')}
        - Nguoi thuc hien: {thong_tin.get('nguoi_thuc_hien', 'Chua chi dinh')}
        - Ghi chu: {thong_tin.get('ghi_chu', 'Khong co')}
        """
        
        noi_dung_word += f"""
        === V. THEO DOI & PHOI HOP ===
        Chu ky xem xet lai: {chu_ky_danh_gia if 'chu_ky_danh_gia' in locals() else 'Moi thang'}
        Ngay du kien xem xet lai: {ngay_danh_gia_lai.strftime('%d/%m/%Y') if 'ngay_danh_gia_lai' in locals() and ngay_danh_gia_lai else 'Chua dat'}
        
        Phoi hop gia dinh - truong:
        {nguoi_phu_hop if 'nguoi_phu_hop' in locals() else 'Chua ghi nhan'}
        
        KY XAC NHAN:
        Nguoi lap ke hoach: _______________    Ngay: _______________
        Phu huynh/Dai dien gia dinh: _______________    Ngay: _______________
        """
        
        tep_word = BytesIO()
        tep_word.write(noi_dung_word.encode('utf-8'))
        tep_word.seek(0)
        
        st.download_button(
            label="📥 Tai ke hoach ra tep Word (.doc)",
            data=tep_word,
            file_name=f"KeHoach_{ten_tre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.doc",
            mime="application/msword"
        )
        st.info("💡 Tep da tai ve may — mo bang Word de chinh sua, in ra de dang!")
        
        st.markdown("---")
        
        # ==== LƯU KẾ HOẠCH VÀO LỊCH SỬ ====
        st.markdown("### 💾 Lưu kế hoạch tự chỉnh sửa")
        if st.button("💾 Lưu vào lịch sử"):
            ke_hoach = {
                "ngay": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "loai": "Kế hoạch hỗ trợ cá nhân",
                "ten_tre": ten_tre,
                "tuoi": tuoi_tre,
                "ngay_sinh": str(ngay_sinh),
                "nguoi_lap": nguoi_lap,
                "diem_manh": diem_manh,
                "linh_vuc_uu_tien": linh_vuc_can_ho_tro,
                "muc_do_ho_tro": muc_do
            }
            st.session_state.lich_su_danh_gia.append(ke_hoach)
            st.success("✅ Đã lưu kế hoạch thành công! Xem lại tại tab 'Lịch sử đánh giá'")
            # Liên kết xem kế hoạch đã lưu
        st.markdown("---")
        st.info("💡 Xem lại tất cả kế hoạch đã tạo tại tab **'📊 Lịch sử đánh giá'** ở thanh bên trái!")
# ==================== TAB 4: TÀI NGUYÊN TRÒ CHƠI ====================
# ==================== TAB 4: TÀI NGUYÊN TRÒ CHƠI ====================
elif tab_chon == "🎮 Tài nguyên trò chơi":
    st.subheader("🎮 Thư viện Trò chơi Học tập Mầm Non")
    st.info("📚 Kho trò chơi theo độ tuổi và lĩnh vực phát triển — Dễ chuẩn bị, hiệu quả!")
    
    # ==== BỘ LỌC ====
    col1, col2 = st.columns(2)
    with col1:
        loc_tuoi = st.selectbox("🔍 Chọn độ tuổi:",
            ["Tất cả", "18–24 tháng", "25–36 tháng"])
    with col2:
        loc_linh_vuc = st.selectbox("📂 Chọn lĩnh vực:",
            ["Tất cả", "Ngôn ngữ & Giao tiếp", "Vận động tinh", "Vận động thô",
             "Giải quyết vấn đề", "Kỹ năng xã hội", "Tự phục vụ", "Âm nhạc & Nghệ thuật"])
    
    st.divider()
    
    # ==== DỮ LIỆU TRÒ CHƠI ====
    danh_sach_tro_choi = [
        # === 18–24 tháng ===
        {
            "ten": "🔊 Nghe và Lặp lại",
            "tuoi": ["18–24 tháng"],
            "linh_vuc": "Ngôn ngữ & Giao tiếp",
            "muc_tieu": "Khuyến khích trẻ phát âm, bắt chước lời nói và tăng vốn từ",
            "cach_choi": """**Chuẩn bị:**
- Không cần đồ vật đặc biệt, có thể kết hợp với đồ vật trong nhà

**Cách chơi:**
1. Đối mặt với trẻ, nói từ đơn giản rõ ràng: 'Bóng', 'Nước', 'Ăn'
2. Mỉm cười, chỉ vào đồ vật khi nói từ đó
3. Khuyến khích trẻ bắt chước — dù chỉ phát âm một phần cũng khen ngợi
4. Lặp lại nhiều lần, thay đổi ngữ điệu vui vẻ

**Thời lượng:** 5–10 phút mỗi lần
**Tần suất:** Hàng ngày, xen kẽ trong sinh hoạt
**Lưu ý:** Không yêu cầu trẻ nói đúng hoàn toàn — quan trọng là sự cố gắng và niềm vui giao tiếp""",
            "nguyen_lieu": "Không cần vật liệu đặc biệt",
            "do_kho": "⭐ Dễ nhất"
        },
        {
            "ten": "✋ Nhặt Đồ Vật Nhỏ",
            "tuoi": ["18–24 tháng"],
            "linh_vuc": "Vận động tinh",
            "muc_tieu": "Rèn kỹ năng nhặt vật bằng ngón cái và ngón trỏ, phối hợp tay-mắt",
            "cach_choi": """**Chuẩn bị:**
- Các vật an toàn, kích thước nhỏ: hạt nhựa lớn, nút áo to, quả bóng xốp nhỏ, nắp chai
- Một cái hộp/khay trống

**Cách chơi:**
1. Đặt các vật ra khay, chỉ cho trẻ xem cách nhặt bằng ngón cái + ngón trỏ
2. Khuyến khích trẻ nhặt từng vật bỏ vào hộp
3. Khi trẻ làm được, khen ngợi nhiệt tình
4. Tăng độ khó: gọi tên vật để trẻ nhặt đúng loại

**Thời lượng:** 5–8 phút
**Tần suất:** 2–3 lần/tuần
**An toàn:** Luôn giám sát — tránh trẻ bỏ vào miệng""",
            "nguyen_lieu": "Hạt nhựa/nút áo to, hộp/khay nhựa",
            "do_kho": "⭐ Dễ nhất"
        },
        {
            "ten": "🚶 Đi theo Đường Kẻ",
            "tuoi": ["18–24 tháng"],
            "linh_vuc": "Vận động thô",
            "muc_tieu": "Rèn thăng bằng, phối hợp chân và tự tin di chuyển",
            "cach_choi": """**Chuẩn bị:**
- Băng dính hoặc phấn vẽ một đường thẳng/đường cong trên sàn nhà

**Cách chơi:**
1. Bước đi trên đường kẻ — tay có thể dang ra để thăng bằng
2. Đầu tiên người lớn nắm tay trẻ, sau đó từ từ nhả ra
3. Hát bài hát đơn giản khi đi để tạo niềm vui
4. Thử đi theo đường cong, đường vòng đơn giản

**Thời lượng:** 10–15 phút
**Tần suất:** 2–3 lần/tuần
**Không gian:** Cần không gian sạch sẽ, bằng phẳng""",
            "nguyen_lieu": "Băng dính/Phấn màu",
            "do_kho": "⭐ Dễ nhất"
        },
        {
            "ten": "🙏 Tìm Đồ Vật Bị Che",
            "tuoi": ["18–24 tháng"],
            "linh_vuc": "Giải quyết vấn đề",
            "muc_tieu": "Phát triển trí nhớ, tư duy tìm kiếm và sự kiên trì",
            "cach_choi": """**Chuẩn bị:**
- Một món đồ trẻ yêu thích, một chiếc khăn/miếng vải nhẹ

**Cách chơi:**
1. Cho trẻ xem rõ đồ vật
2. Dùng khăn che hoàn toàn đồ vật trước mặt trẻ
3. Hỏi: 'Đồ vật đâu rồi? Con tìm xem!'
4. Khi trẻ tìm thấy, khen ngợi nhiệt tình: 'Con thông minh quá!'
5. Tăng độ khó: che ở nhiều nơi khác nhau

**Thời lượng:** 5–10 phút
**Tần suất:** 2–3 lần/tuần""",
            "nguyen_lieu": "Đồ vật quen thuộc, khăn vải nhẹ",
            "do_kho": "⭐ Dễ nhất"
        },
        {
            "ten": "🤗 Chào Hỏi & Biểu Cảm",
            "tuoi": ["18–24 tháng"],
            "linh_vuc": "Kỹ năng xã hội",
            "muc_tieu": "Hình thành thói quen giao tiếp thân thiện, nhận biết cảm xúc",
            "cach_choi": """**Chuẩn bị:**
- Không cần vật liệu — thực hiện trong giao tiếp hàng ngày

**Cách chơi:**
1. Khi gặp người: mỉm cười, vẫy tay nói 'Xin chào'
2. Khi tạm biệt: vẫy tay nói 'Tạm biệt'
3. Dạy trẻ ôm nhẹ khi gặp người thân
4. Chỉ vào ảnh/người và nói: 'Bạn đang vui', 'Bạn đang buồn'

**Thời lượng:** Thực hiện trong mọi tình huống hàng ngày
**Tần suất:** Mọi lúc, mọi nơi""",
            "nguyen_lieu": "Không cần vật liệu",
            "do_kho": "⭐ Dễ nhất"
        },
        
        # === 25–36 tháng ===
        {
            "ten": "📖 Kể Truyện Theo Hình Ảnh",
            "tuoi": ["25–36 tháng"],
            "linh_vuc": "Ngôn ngữ & Giao tiếp",
            "muc_tieu": "Rèn khả năng diễn đạt, nối câu và tư duy logic",
            "cach_choi": """**Chuẩn bị:**
- Sách ảnh đơn giản hoặc bộ thẻ hình có trình tự sự việc

**Cách chơi:**
1. Xem từng hình, hỏi trẻ: 'Con thấy gì trong ảnh?'
2. Khuyến khích trẻ nói bằng 2–3 từ: 'Đây là con chó', 'Chó đang chạy'
3. Nối các hình thành một câu chuyện ngắn
4. Để trẻ tự kể lại theo cách của mình

**Thời lượng:** 10–15 phút
**Tần suất:** 2–3 lần/tuần
**Lưu ý:** Không sửa lỗi trực tiếp — nhắc lại đúng mẫu sau đó""",
            "nguyen_lieu": "Sách ảnh/Thẻ hình đơn giản",
            "do_kho": "⭐⭐ Trung bình"
        },
        {
            "ten": "🎨 Tô Màu & Vẽ Theo Mẫu",
            "tuoi": ["25–36 tháng"],
            "linh_vuc": "Vận động tinh",
            "muc_tieu": "Kiểm soát cử động tay-phát triển phối hợp tay-mắt, nhận biết màu sắc",
            "cach_choi": """**Chuẩn bị:**
- Giấy trắng, bút chì màu/sáp màu to dễ cầm
- Hình vẽ sẵn nét viền đậm, kích thước lớn

**Cách chơi:**
1. Chỉ cho trẻ cách cầm bút đúng (không cần quá nghiêm ngặt)
2. Tô màu trong khung — không yêu cầu đều màu
3. Nêu tên màu sắc khi trẻ tô
4. Vẽ theo mẫu đơn giản: đường thẳng, vòng tròn

**Thời lượng:** 10–15 phút
**Tần suất:** 2–3 lần/tuần
**An toàn:** Dùng bút màu không độc hại, dễ rửa sạch""",
            "nguyen_lieu": "Giấy, bút chì màu/bút sáp to",
            "do_kho": "⭐⭐ Trung bình"
        },
        {
            "ten": "⚽ Đá & Ném Bóng",
            "tuoi": ["25–36 tháng"],
            "linh_vuc": "Vận động thô",
            "muc_tieu": "Phối hợp tay-chân, thăng bằng, định hướng không gian",
            "cach_choi": """**Chuẩn bị:**
- Bóng mềm, kích thước phù hợp với tay/trẻ

**Cách chơi:**
1. Ném bóng cho người khác — hai tay trước ngực
2. Đá bóng nhẹ về phía trước — theo hướng chỉ định
3. Chạy theo bóng rồi dừng lại an toàn
4. Bắt bóng lớn với hai tay ôm

**Thời lượng:** 15–20 phút
**Tần suất:** Hàng ngày nếu có điều kiện
**Không gian:** Ngoài trời hoặc phòng rộng, không vật cản nguy hiểm""",
            "nguyen_lieu": "Bóng mềm kích thước trung bình",
            "do_kho": "⭐⭐ Trung bình"
        },
        {
            "ten": "🧩 Phân Loại Đồ Vật",
            "tuoi": ["25–36 tháng"],
            "linh_vuc": "Giải quyết vấn đề",
            "muc_tieu": "Phát triển tư duy logic — phân loại theo màu sắc, hình dạng, kích thước",
            "cach_choi": """**Chuẩn bị:**
- Các đồ vật an toàn: khối gỗ, đồ chơi, nắp chai, thìa nhựa...
- 2–3 cái hộp/khay khác màu nhau

**Cách chơi:**
1. Chia theo màu sắc: 'Đặt tất cả vật màu đỏ vào hộp này'
2. Chia theo hình dạng: 'Đặt vật tròn vào đây, vật vuông vào kia'
3. Chia theo chức năng: 'Đồ vật dùng để ăn ở đâu?'
4. Khen ngợi khi trẻ làm đúng, nhẹ nhàng hướng dẫn khi chưa đúng

**Thời lượng:** 10–15 phút
**Tần suất:** 2–3 lần/tuần""",
            "nguyen_lieu": "Đồ vật đa dạng, hộp/khay phân loại",
            "do_kho": "⭐⭐ Trung bình"
        },
        {
            "ten": "🤝 Chia Sẻ & Chơi Cùng",
            "tuoi": ["25–36 tháng"],
            "linh_vuc": "Kỹ năng xã hội",
            "muc_tieu": "Học chơi cùng bạn, chờ đến lượt và chia sẻ đồ vật",
            "cach_choi": """**Chuẩn bị:**
- Nhóm 2–3 trẻ, bộ đồ chơi đủ chia sẻ

**Cách chơi:**
1. Ngồi thành vòng tròn, truyền đồ chơi cho bạn bên cạnh
2. Hướng dẫn: 'Đến lượt con rồi', 'Chờ bạn xong đến lượt con'
3. Khi trẻ chia sẻ, khen ngợi ngay: 'Con chia sẻ tốt quá!'
4. Trò chơi luân phiên: lăn bóng cho bạn rồi nhận lại

**Thời lượng:** 15–20 phút
**Tần suất:** Hàng ngày trong hoạt động nhóm""",
            "nguyen_lieu": "Đồ chơi nhóm, không cần vật liệu đặc biệt",
            "do_kho": "⭐⭐ Trung bình"
        },
        {
            "ten": "🧦 Tự Mặc Quần Áo",
            "tuoi": ["25–36 tháng"],
            "linh_vuc": "Tự phục vụ",
            "muc_tieu": "Rèn sự độc lập, tự tin và kỹ năng tự chăm sóc bản thân",
            "cach_choi": """**Chuẩn bị:**
- Quần áo đơn giản của trẻ: dép, tất, áo có lỗ rộng, quần co giãn

**Cách chơi:**
1. Xem như một trò chơi thú vị, không tạo áp lực
2. Hướng dẫn từng bước chậm rãi: tay vào tay áo, chân vào chân quần
3. Để trẻ cố gắng trước — chỉ giúp khi trẻ thực sự cần
4. Khen ngợi nỗ lực dù chưa hoàn hảo

**Thời lượng:** Thực hiện mỗi sáng/chiều khi thay đồ
**Tần suất:** Hàng ngày
**Lưu ý:** Kiên nhẫn — trẻ cần nhiều thời gian hơn người lớn""",
            "nguyen_lieu": "Quần áo, dép, tất của trẻ",
            "do_kho": "⭐⭐ Trung bình"
        },
        {
            "ten": "🎵 Nghe Nhạc & Vận Động",
            "tuoi": ["18–24 tháng", "25–36 tháng"],
            "linh_vuc": "Âm nhạc & Nghệ thuật",
            "muc_tieu": "Phát triển thính giác, nhịp điệu, cảm xúc và phối hợp vận động",
            "cach_choi": """**Chuẩn bị:**
- Bài hát thiếu nhi có giai điệu vui, rõ nhịp điệu
- Có thể dùng nhạc cụ đơn giản: trống nhựa, thanh gõ, lục lạc

**Cách chơi:**
1. Nghe nhạc — vỗ tay theo nhịp
2. Di chuyển cơ thể theo nhạc: nhảy, xoay, vung tay
3. Dùng nhạc cụ đơn giản tạo âm thanh cùng nhạc
4. Bắt chước hành động trong bài hát

**Thời lượng:** 10–15 phút
**Tần suất:** Hàng ngày
**Lưu ý:** Giữ âm lượng ở mức vừa phải, an toàn cho tai trẻ""",
            "nguyen_lieu": "Nhạc thiếu nhi, nhạc cụ đơn giản (tùy chọn)",
            "do_kho": "⭐ Dễ nhất"
        },
        {
            "ten": "✂️ Xé & Dán Giấy",
            "tuoi": ["25–36 tháng"],
            "linh_vuc": "Vận động tinh + Sáng tạo",
            "muc_tieu": "Rèn cơ ngón tay, sức bền tay và khả năng sáng tạo",
            "cach_choi": """**Chuẩn bị:**
- Giấy màu mềm, giấy vụn sạch
- Keo dán an toàn, que chấm keo
- Giấy trắng làm nền

**Cách chơi:**
1. Xé giấy thành các mảnh nhỏ theo ý muốn
2. Chấm keo vào mặt sau mảnh giấy
3. Dán lên giấy nền tạo thành hình ảnh đơn giản
4. Nêu tên những gì trẻ tạo ra

**Thời lượng:** 15–20 phút
**Tần suất:** 1–2 lần/tuần
**An toàn:** Giấy không quá nhỏ, không để trẻ bỏ vào miệng""",
            "nguyen_lieu": "Giấy màu, keo dán an toàn, giấy nền",
            "do_kho": "⭐⭐ Trung bình"
        }
    ]
    
    # ==== LỌC & HIỂN THỊ ====
    tro_choi_loc = []
    for tc in danh_sach_tro_choi:
        loc_ok = True
        if loc_tuoi != "Tất cả" and loc_tuoi not in tc["tuoi"]:
            loc_ok = False
        if loc_linh_vuc != "Tất cả" and tc["linh_vuc"] != loc_linh_vuc:
            loc_ok = False
        if loc_ok:
            tro_choi_loc.append(tc)
    
    if tro_choi_loc:
        st.success(f"✅ Tìm thấy {len(tro_choi_loc)} trò chơi phù hợp!")
        
        for i, tc in enumerate(tro_choi_loc, 1):
            with st.expander(f"🎮 {i}. {tc['ten']} — {tc['linh_vuc']}"):
                st.markdown(f"""
                **👶 Độ tuổi:** {', '.join(tc['tuoi'])}  |  **{tc['do_kho']}**
                
                ### 🎯 Mục tiêu:
                {tc['muc_tieu']}
                
                ### 📋 Nguyên liệu cần chuẩn bị:
                {tc['nguyen_lieu']}
                
                ### 🎲 Cách chơi chi tiết:
                {tc['cach_choi']}
                """)
    else:
        st.info("🔍 Không tìm thấy trò chơi phù hợp. Vui lòng thay đổi bộ lọc!")
    
    st.divider()
    
    # ==== TẠO TRÒ CHƠI CỦA BẠN ====
    st.markdown("### ✏️ Thêm trò chơi mới của bạn")
    with st.form("form_them_tro_choi"):
        ten_moi = st.text_input("Tên trò chơi:")
        tuoi_moi = st.multiselect("Độ tuổi phù hợp:", ["18–24 tháng", "25–36 tháng"])
        linh_vuc_moi = st.selectbox("Lĩnh vực phát triển:",
            ["Ngôn ngữ & Giao tiếp", "Vận động tinh", "Vận động thô",
             "Giải quyết vấn đề", "Kỹ năng xã hội", "Tự phục vụ", "Âm nhạc & Nghệ thuật"])
        muc_tieu_moi = st.text_area("Mục tiêu phát triển:")
        nguyen_lieu_moi = st.text_input("Nguyên liệu cần chuẩn bị:")
        cach_choi_moi = st.text_area("Cách chơi chi tiết:")
        
        if st.form_submit_button("💾 Lưu trò chơi"):
            if ten_moi and tuoi_moi:
                st.success(f"✅ Đã lưu trò chơi: **{ten_moi}** — Bạn có thể thêm vào danh sách chính thức sau nhé!")
            else:
                st.warning("⚠️ Vui lòng nhập tên trò chơi và chọn độ tuổi!")
# ==================== TAB 5: LỊCH SỬ ĐÁNH GIÁ ====================
# ==================== TAB 5: LỊCH SỬ & HỒ SƠ ĐÃ LƯU ====================
elif tab_chon == "📊 Lịch sử đánh giá":
    st.subheader("📊 Hồ sơ lưu trữ & Lịch sử theo dõi")
    st.info(f"Tổng số hồ sơ đã lưu: **{len(st.session_state.lich_su_danh_gia)}**")
    
    if not st.session_state.lich_su_danh_gia:
        st.info("📋 Chưa có hồ sơ nào được lưu. Hoàn thành đánh giá hoặc tạo kế hoạch để lưu kết quả nhé!")
    else:
        # Tạo bộ lọc
        col_loc1, col_loc2 = st.columns(2)
        with col_loc1:
            loc_loai = st.selectbox("Lọc theo loại hồ sơ:", 
                ["Tất cả"] + list(set([hs.get('loai_danh_gia', hs.get('loai', 'Khác')) 
                     for hs in st.session_state.lich_su_danh_gia])))
        with col_loc2:
            loc_tre = st.selectbox("Lọc theo trẻ:",
                ["Tất cả"] + list(set([hs.get('ten_tre', 'Không ghi tên') 
                     for hs in st.session_state.lich_su_danh_gia])))
        
        st.markdown("---")
        
        # Lọc danh sách
        ds_hs_hien_thi = []
        for hs in reversed(st.session_state.lich_su_danh_gia):
            hien_thi = True
            if loc_loai != "Tất cả":
                loai_hs = hs.get('loai_danh_gia', hs.get('loai', ''))
                if loc_loai not in loai_hs:
                    hien_thi = False
            if loc_tre != "Tất cả":
                if hs.get('ten_tre', '') != loc_tre:
                    hien_thi = False
            if hien_thi:
                ds_hs_hien_thi.append(hs)
        
        if not ds_hs_hien_thi:
            st.info("🔍 Không tìm thấy hồ sơ phù hợp với điều kiện lọc!")
        else:
            st.success(f"✅ Tìm thấy {len(ds_hs_hien_thi)} hồ sơ")
            
            # Hiển thị danh sách với nút xem chi tiết
            for chi_so, hs in enumerate(ds_hs_hien_thi):
                ten_tre = hs.get('ten_tre', 'Không ghi tên')
                ngay = hs.get('ngay', 'Không rõ ngày')
                loai = hs.get('loai_danh_gia', hs.get('loai', 'Hồ sơ'))
                tuoi = hs.get('tuoi', '')
                
                with st.expander(f"📅 {ngay} — {ten_tre} ({tuoi}) | {loai}", expanded=False):
                    st.markdown("#### 📄 Thông tin hồ sơ")
                    st.write(f"**Ngày tạo:** {ngay}")
                    st.write(f"**Tên trẻ:** {ten_tre}")
                    if tuoi:
                        st.write(f"**Độ tuổi:** {tuoi}")
                    
                    st.markdown("---")
                    
                    # Hiển thị nội dung theo loại hồ sơ
                    loai_hs = hs.get('loai_danh_gia', hs.get('loai', ''))
                    
                    if "Sàng lọc sớm" in loai_hs:
                        st.markdown("#### 🔍 Kết quả Sàng lọc sớm")
                        st.write(f"- **Tổng dấu hiệu:** {hs.get('dau_hieu_tong', 'Không ghi')}")
                        st.write(f"- **Chưa thể hiện:** {hs.get('dau_hieu_chua_dat', 'Không ghi')}")
                        if 'chi_tiet' in hs:
                            with st.expander("Xem chi tiết từng dấu hiệu"):
                                for ten_dh, da_dat in hs['chi_tiet'].items():
                                    trang_thai = "✅ Đạt" if da_dat else "❌ Chưa đạt"
                                    st.write(f"- {trang_thai}: {ten_dh}")
                    
                    elif "Kế hoạch hỗ trợ cá nhân" in loai_hs:
                        st.markdown("#### 📋 Thông tin Kế hoạch cá nhân")
                        st.write(f"**Người lập:** {hs.get('nguoi_lap', 'Không ghi')}")
                        st.write(f"**Điểm mạnh:** {hs.get('diem_manh', 'Chưa ghi nhận')}")
                        lnv = hs.get('linh_vuc_can_ho_tro', hs.get('linh_vuc_uu_tien', []))
                        st.write(f"**Lĩnh vực ưu tiên hỗ trợ:** {', '.join(lnv) if lnv else 'Chưa chọn'}")
                        st.write(f"**Mức độ hỗ trợ:** {hs.get('muc_do_ho_tro', 'Không ghi')}")
                        st.write(f"**Mô tả khó khăn:** {hs.get('mo_ta_kho_khan', 'Chưa mô tả')}")
                    
                    else: # Đánh giá ASQ-3
                        st.markdown("#### 📊 Kết quả Đánh giá ASQ-3")
                        if 'diem' in hs:
                            for linh_vuc, diem in hs['diem'].items():
                                st.metric(label=linh_vuc, value=f"{diem}/60")
                                st.progress(diem / 60)
                                # Đánh giá nhanh
                                if diem >= 50:
                                    st.success("✅ Phát triển tốt")
                                elif 30 <= diem < 50:
                                    st.warning("⚠️ Cần theo dõi")
                                else:
                                    st.error("🔴 Cần hỗ trợ thêm")
                                st.markdown("---")
                    
                    # Nút xóa hồ sơ
                    if st.button(f"🗑️ Xóa hồ sơ này", key=f"xoa_{chi_so}_{ngay}"):
                        st.session_state.lich_su_danh_gia.remove(hs)
                        st.success("✅ Đã xóa hồ sơ! Tải lại trang để cập nhật danh sách.")
                        st.rerun()
