import streamlit as st
import os
from datetime import datetime

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
    
    # ==== THÊM TRẺ MỚI ====
    with st.expander("➕ Thêm trẻ mới"):
        ten_tre_moi = st.text_input("Tên trẻ:")
        ngay_sinh_moi = st.date_input("Ngày sinh:")
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

# ==================== TAB 2: SÀNG LỌC SỚM ====================
elif tab_chon == "🔍 Sàng lọc sớm":
    st.subheader("🔍 Bảng theo dõi dấu hiệu phát triển")
    st.info("Chức năng đang được phát triển. Vui lòng quay lại sau!")

# ==================== TAB 3: KẾ HOẠCH CÁ NHÂN ====================
elif tab_chon == "📄 Tạo kế hoạch cá nhân":
    st.subheader("📄 Kế hoạch hỗ trợ cá nhân")
    st.info("Chức năng đang được phát triển. Vui lòng quay lại sau!")

# ==================== TAB 4: TÀI NGUYÊN TRÒ CHƠI ====================
elif tab_chon == "🎮 Tài nguyên trò chơi":
    st.subheader("🎮 Trò chơi học tập theo độ tuổi")
    st.info("Chức năng đang được phát triển. Vui lòng quay lại sau!")

# ==================== TAB 5: LỊCH SỬ ĐÁNH GIÁ ====================
elif tab_chon == "📊 Lịch sử đánh giá":
    st.subheader("📊 Lịch sử đánh giá")
    if st.session_state.lich_su_danh_gia:
        st.info(f"Tổng số đánh giá đã lưu: {len(st.session_state.lich_su_danh_gia)}")
        for i, ket_qua in enumerate(reversed(st.session_state.lich_su_danh_gia), 1):
            with st.expander(f"📅 {ket_qua['ngay']} — {ket_qua['ten_tre']} ({ket_qua['tuoi']})"):
                st.write("**Người đánh giá:**", ket_qua.get('nguoi_danh_gia', 'Không ghi'))
                for linh_vuc, diem in ket_qua['diem'].items():
                    st.write(f"- **{linh_vuc}:** {diem}/60 điểm")
    else:
        st.info("Chưa có lịch sử đánh giá nào. Hoàn thành một đánh giá ở tab 'Đánh giá ASQ-3' để lưu kết quả nhé!")
