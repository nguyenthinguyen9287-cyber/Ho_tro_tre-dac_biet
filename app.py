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
# ==================== TAB 2: SÀNG LỌC SỚM ====================
elif tab_chon == "🔍 Sàng lọc sớm":
    st.subheader("🔍 Bảng sàng lọc dấu hiệu phát triển trẻ mầm non")
    st.info("Danh mục các dấu hiệu cần quan sát — Phát hiện sớm những khó khăn có thể có của trẻ")
    
    # Chọn độ tuổi phù hợp
    nhom_tuoi_sang_loc = st.selectbox("Chọn nhóm độ tuổi cần sàng lọc:", 
                                        ["18–24 tháng", "25–36 tháng"])
    
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

# ==================== TAB 3: KẾ HOẠCH CÁ NHÂN ====================
# ==================== TAB 3: KẾ HOẠCH CÁ NHÂN ====================
elif tab_chon == "📄 Tạo kế hoạch cá nhân":
    st.subheader("📄 Kế hoạch hỗ trợ phát triển cá nhân cho trẻ")
    
    if not st.session_state.tre_hien_tai:
        st.warning("⚠️ Vui lòng chọn trẻ ở thanh bên trái trước khi lập kế hoạch!")
    else:
        tre = st.session_state.tre_hien_tai
        ten_tre = tre.get('ten', 'Trẻ')
        tuoi_tre = tre.get('tuoi', '')
        ngay_sinh = tre.get('ngay_sinh', '')
        nguoi_lap = st.text_input("Người lập kế hoạch:", value=tre.get('nguoi_danh_gia', ''))
        ngay_lap = datetime.now().strftime("%d/%m/%Y")
        
        st.info(f"📋 Lập kế hoạch cho: **{ten_tre}** — {tuoi_tre}")
        st.divider()
        
        # ==== Thông tin chung & Điểm mạnh ====
        st.markdown("### 💪 Điểm mạnh của trẻ")
        diem_manh = st.text_area("Trẻ có những khả năng/điểm mạnh nào?", 
            placeholder="Ví dụ: Trẻ rất thân thiện, thích giao tiếp với bạn bè, nhớ nhanh bài hát...", height=100)
        
        st.markdown("### 🔍 Lĩnh vực cần hỗ trợ thêm")
        linh_vuc_can_ho_tro = st.multiselect("Chọn lĩnh vực cần tập trung hỗ trợ:",
            ["Ngôn ngữ & Giao tiếp", "Vận động tinh", "Vận động thô", 
             "Giải quyết vấn đề", "Kỹ năng xã hội", "Tự phục vụ", "Chú ý & Hành vi"])
        
        mo_ta_kho_khan = st.text_area("Mô tả cụ thể những khó khăn trẻ đang gặp:",
            placeholder="Ví dụ: Trẻ chưa tự tin nói trước nhóm, hay ngại giao tiếp bằng mắt...", height=120)
        
        st.divider()
        
        # ==== Mục tiêu hỗ trợ ====
        st.markdown("### 🎯 Mục tiêu hỗ trợ")
        muc_tieu_ngan_han = st.text_area("Mục tiêu ngắn hạn (1–3 tháng):",
            placeholder="Ví dụ: Trẻ tự giới thiệu được tên mình khi được hỏi", height=80)
        muc_tieu_dai_han = st.text_area("Mục tiêu dài hạn (6–12 tháng):",
            placeholder="Ví dụ: Trẻ tự tin giao tiếp với bạn bè và người xung quanh", height=80)
        
        st.divider()
        
        # ==== Giải pháp hỗ trợ theo lĩnh vực ====
        st.markdown("### 🛠️ Giải pháp hỗ trợ cụ thể")
        
        giai_phap = {}
        for linh_vuc in linh_vuc_can_ho_tro:
            with st.expander(f"📌 Hoạt động hỗ trợ: {linh_vuc}"):
                hoat_dong = st.text_area(f"Các hoạt động thường xuyên:",
                    placeholder="Liệt kê hoạt động, trò chơi phù hợp với trẻ",
                    key=f"hd_{linh_vuc}", height=100)
                tan_suat = st.select_slider(f"Tần suất thực hiện:",
                    options=["1 lần/ngày", "2–3 lần/tuần", "Hàng ngày", "Theo nhu cầu"],
                    key=f"ts_{linh_vuc}")
                nguoi_thuc_hien = st.text_input(f"Người chịu trách nhiệm:",
                    placeholder="Giáo viên / Phụ huynh", key=f"nguoi_{linh_vuc}")
                ghi_chu = st.text_area(f"Ghi chú & điều chỉnh:",
                    placeholder="Cách điều chỉnh khi trẻ chưa tham gia...",
                    key=f"gc_{linh_vuc}", height=80)
                
                giai_phap[linh_vuc] = {
                    "hoat_dong": hoat_dong,
                    "tan_suat": tan_suat,
                    "nguoi_thuc_hien": nguoi_thuc_hien,
                    "ghi_chu": ghi_chu
                }
        
        st.divider()
        
        # ==== Thời gian theo dõi & đánh giá lại ====
        st.markdown("### 📅 Theo dõi và đánh giá lại")
        chu_ky_danh_gia = st.selectbox("Chu kỳ xem xét lại kế hoạch:",
            ["Mỗi tháng", "Mỗi 2 tháng", "Mỗi quý", "Sau 6 tháng"])
        ngay_danh_gia_lai = st.date_input("Ngày dự kiến xem xét lại kế hoạch:")
        nguoi_phu_hop = st.text_area("Cách phối hợp giữa gia đình và trường:",
            placeholder="Thông tin trao đổi, cách theo dõi chung...", height=100)
        
        st.divider()
        
        # ==== Xem trước & Lưu kế hoạch ====
        if st.button("📄 Xem trước kế hoạch hoàn chỉnh"):
            st.markdown("---")
            st.markdown(f"""
            # 📋 KẾ HOẠCH HỖ TRỢ PHÁT TRIỂN CÁ NHÂN
            **Tên trẻ:** {ten_tre}  |  **Ngày sinh:** {ngay_sinh}  |  **Nhóm tuổi:** {tuoi_tre}
            **Ngày lập:** {ngay_lap}  |  **Người lập:** {nguoi_lap}
            
            ---
            
            ## 💪 Điểm mạnh của trẻ
            {diem_manh or '*Chưa ghi nhận*'}
            
            ---
            
            ## 🔍 Lĩnh vực cần hỗ trợ thêm
            {', '.join(linh_vuc_can_ho_tro) or '*Chưa chọn lĩnh vực*'}
            
            **Mô tả khó khăn:**
            {mo_ta_kho_khan or '*Chưa mô tả chi tiết*'}
            
            ---
            
            ## 🎯 Mục tiêu hỗ trợ
            **Mục tiêu ngắn hạn (1–3 tháng):**
            {muc_tieu_ngan_han or '*Chưa đặt mục tiêu*'}
            
            **Mục tiêu dài hạn (6–12 tháng):**
            {muc_tieu_dai_han or '*Chưa đặt mục tiêu*'}
            
            ---
            
            ## 🛠️ Giải pháp hỗ trợ cụ thể
            """)
            
            for lv, thong_tin in giai_phap.items():
                st.markdown(f"""
                **📌 {lv}**
                - *Hoạt động:* {thong_tin['hoat_dong'] or '*Chưa mô tả*'}
                - *Tần suất:* {thong_tin['tan_suat']}
                - *Người thực hiện:* {thong_tin['nguoi_thuc_hien'] or '*Chưa chỉ định*'}
                - *Ghi chú:* {thong_tin['ghi_chu'] or '*Không có*'}
                """)
            
            st.markdown(f"""
            ---
            
            ## 📅 Theo dõi và đánh giá lại
            - **Chu kỳ xem xét lại:** {chu_ky_danh_gia}
            - **Ngày dự kiến xem xét lại:** {ngay_danh_gia_lai.strftime('%d/%m/%Y')}
            - **Phối hợp gia đình – trường:**
            {nguoi_phu_hop or '*Chưa ghi nhận*'}
            
            ---
            **Ký xác nhận:**
            Người lập kế hoạch: _______________  Ngày: _______________
            Phụ huynh/Đại diện gia đình: _______________  Ngày: _______________
            """)
            st.markdown("---")
        
        if st.button("💾 Lưu kế hoạch vào lịch sử"):
            ke_hoach = {
                "ngay": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "loai": "Kế hoạch hỗ trợ cá nhân",
                "ten_tre": ten_tre,
                "tuoi": tuoi_tre,
                "nguoi_lap": nguoi_lap,
                "diem_manh": diem_manh,
                "linh_vuc_can_ho_tro": linh_vuc_can_ho_tro,
                "mo_ta_kho_khan": mo_ta_kho_khan,
                "muc_tieu_ngan_han": muc_tieu_ngan_han,
                "muc_tieu_dai_han": muc_tieu_dai_han,
                "giai_phap": giai_phap,
                "chu_ky_danh_gia": chu_ky_danh_gia,
                "ngay_danh_gia_lai": ngay_danh_gia_lai.strftime("%d/%m/%Y"),
                "phoi_hop": nguoi_phu_hop
            }
            st.session_state.lich_su_danh_gia.append(ke_hoach)
            st.success("✅ Đã lưu kế hoạch thành công! Xem tại tab 'Lịch sử đánh giá' nhé! 🎉")

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
