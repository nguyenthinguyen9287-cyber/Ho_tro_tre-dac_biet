import streamlit as st
import os
import io
from datetime import datetime

# ===================== CẤU HÌNH TRANG =====================
st.set_page_config(
    page_title="Trợ Lý Giáo Viên Mầm Non",
    page_icon="👶",
    layout="wide"
)

# ===================== KHỞI TẠO DỮ LIỆU =====================
if 'danh_sach_tre' not in st.session_state:
    st.session_state.danh_sach_tre = []
if 'tre_hien_tai' not in st.session_state:
    st.session_state.tre_hien_tai = None
if 'ket_qua_sang_loc' not in st.session_state:
    st.session_state.ket_qua_sang_loc = {}

# ===================== DỮ LIỆU SÀNG LỌC THEO ĐỘ TUỔI =====================
DU_LIEU_SANG_LOC = {
    "18-24 tháng": {
        "Ngôn ngữ & Giao tiếp": [
            ("Trẻ có thể chỉ ra đồ vật khi được gọi tên?", False),
            ("Trẻ có thể nói ít nhất 6-10 từ có nghĩa?", False),
            ("Trẻ có thể nói yêu cầu đơn giản không cần chỉ?", False)
        ],
        "Phát triển Vận động": [
            ("Trẻ có thể đi được vững?", False),
            ("Trẻ có thể chạy không bị ngã thường xuyên?", False),
            ("Trẻ có thể ném bóng về phía mục tiêu?", False)
        ],
        "Kỹ năng Xã hội & Tự phục vụ": [
            ("Trẻ thích chơi cạnh bên bạn bè?", False),
            ("Trẻ có thể tự cầm muỗng ăn?", False),
            ("Trẻ có thể tự tháo tất/giày đơn giản?", False)
        ],
        "Nhận thức & Tư duy": [
            ("Trẻ có thể tìm thấy đồ vật bị che giấu?", False),
            ("Trẻ có thể xếp được 2-3 khối gỗ chồng lên nhau?", False),
            ("Trẻ bắt chước hành động đơn giản của người lớn?", False)
        ]
    },
    "25-36 tháng": {
        "Ngôn ngữ & Giao tiếp": [
            ("Trẻ hiểu được chỉ dẫn gồm 2 bước?", False),
            ("Trẻ nói được câu gồm 2-3 từ?", False),
            ("Trẻ có thể trả lời câu hỏi đơn giản 'Đâu?', 'Ai?'?", False)
        ],
        "Phát triển Vận động": [
            ("Trẻ có thể nhảy bằng 2 chân?", False),
            ("Trẻ đi lên/xuống cầu thang không cần nắm?", False),
            ("Trẻ có thể vẽ nét thẳng/tròn?", False)
        ],
        "Kỹ năng Xã hội & Tự phục vụ": [
            ("Trẻ chơi được với bạn bè ít phút?", False),
            ("Trẻ có thể tự rửa tay đơn giản?", False),
            ("Trẻ nói 'tôi tự làm được' khi được giúp?", False)
        ],
        "Nhận thức & Tư duy": [
            ("Trẻ phân biệt được màu cơ bản?", False),
            ("Trẻ phân biệt được to/nhỏ, nhiều/ít?", False),
            ("Trẻ nhớ được nơi để đồ vật thường dùng?", False)
        ]
    },
    "37-48 tháng": {
        "Ngôn ngữ & Giao tiếp": [
            ("Trẻ nói được câu hoàn chỉnh 3-4 từ?", False),
            ("Trẻ kể lại được sự việc đơn giản?", False),
            ("Trẻ hiểu được đối thoại ngắn?", False)
        ],
        "Phát triển Vận động": [
            ("Trẻ chạy nhanh, đổi hướng được?", False),
            ("Trẻ nhảy xa được khoảng 30cm?", False),
            ("Trẻ cầm kéo cắt giấy đơn giản?", False)
        ],
        "Kỹ năng Xã hội & Tự phục vụ": [
            ("Trẻ chia sẻ đồ chơi với bạn?", False),
            ("Trẻ tự mặc/ cởi quần áo đơn giản?", False),
            ("Trẻ biết chờ đến lượt mình?", False)
        ],
        "Nhận thức & Tư duy": [
            ("Trẻ đếm được 1-5?", False),
            ("Trẻ phân biệt được hình tròn, vuông, tam giác?", False),
            ("Trẻ hiểu khái niệm 'giống nhau', 'khác nhau'?", False)
        ]
    },
    "49-60 tháng": {
        "Ngôn ngữ & Giao tiếp": [
            ("Trẻ sử dụng được câu phức?", False),
            ("Trẻ kể chuyện ngắn theo trình tự?", False),
            ("Trẻ trả lời câu hỏi 'Tại sao?'?", False)
        ],
        "Phát triển Vận động": [
            ("Trẻ đi xe đạp 4 bánh tốt?", False),
            ("Trẻ vẽ người đủ bộ phận chính?", False),
            ("Trẻ cầm bút chì đúng tư thế?", False)
        ],
        "Kỹ năng Xã hội & Tự phục vụ": [
            ("Trẻ tuân theo quy tắc trò chơi?", False),
            ("Trẻ tự đi vệ sinh và rửa tay sau đó?", False),
            ("Trẻ biết xin lỗi khi làm sai?", False)
        ],
        "Nhận thức & Tư duy": [
            ("Trẻ đếm được 1-10 và hiểu giá trị số?", False),
            ("Trẻ phân biệt được trên/dưới, trước/sau?", False),
            ("Trẻ nhớ được quy trình đơn giản 3-4 bước?", False)
        ]
    },
    "61-72 tháng": {
        "Ngôn ngữ & Giao tiếp": [
            ("Trẻ giao tiếp tự nhiên với mọi người?", False),
            ("Trẻ kể lại câu chuyện nghe được?", False),
            ("Trẻ diễn đạt được suy nghĩ của mình?", False)
        ],
        "Phát triển Vận động": [
            ("Trẻ chạy, nhảy, ném bóng chính xác hơn?", False),
            ("Trẻ vẽ theo ý muốn và giải thích được?", False),
            ("Trẻ cắt theo đường thẳng/nét cong đơn giản?", False)
        ],
        "Kỹ năng Xã hội & Tự phục vụ": [
            ("Trẻ hợp tác trong hoạt động nhóm?", False),
            ("Trẻ tự chuẩn bị đồ dùng học tập?", False),
            ("Trẻ tự bảo vệ bản thân an toàn cơ bản?", False)
        ],
        "Nhận thức & Tư duy": [
            ("Trẻ nhận biết chữ cái và số quen thuộc?", False),
            ("Trẻ hiểu quy luật đơn giản?", False),
            ("Trẻ giải quyết vấn đề nhỏ theo cách của mình?", False)
        ]
    }
}

# ===================== THANH BÊN TRÁI =====================
with st.sidebar:
    st.title("👶 Quản lý trẻ")
    
    # Thêm trẻ mới
    st.subheader("➕ Thêm trẻ mới")
    ten = st.text_input("Tên trẻ")
    ngay_sinh = st.date_input("Ngày sinh", value=None)
    nhom_tuoi = st.selectbox("Nhóm độ tuổi", list(DU_LIEU_SANG_LOC.keys()))
    
    if st.button("Lưu thông tin trẻ"):
        if ten and ngay_sinh:
            tre_moi = {
                "id": len(st.session_state.danh_sach_tre) + 1,
                "ten": ten,
                "ngay_sinh": ngay_sinh.strftime("%d/%m/%Y"),
                "tuoi": nhom_tuoi,
                "ngay_tao": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.danh_sach_tre.append(tre_moi)
            st.session_state.tre_hien_tai = tre_moi
            st.success(f"✅ Đã thêm: {ten}")
            st.rerun()
        else:
            st.warning("⚠️ Vui lòng nhập tên và chọn ngày sinh!")
    
    # Danh sách trẻ đã lưu
    st.subheader("📋 Danh sách trẻ")
    if st.session_state.danh_sach_tre:
        for idx, tre in enumerate(st.session_state.danh_sach_tre):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"👤 {tre['ten']} — {tre['tuoi']}", key=f"chon_tre_{idx}"):
                    st.session_state.tre_hien_tai = tre
                    st.session_state.ket_qua_sang_loc = {}
                    st.rerun()
            with col2:
                if st.button("❌", key=f"xoa_tre_{idx}"):
                    st.session_state.danh_sach_tre.pop(idx)
                    if st.session_state.tre_hien_tai == tre:
                        st.session_state.tre_hien_tai = None
                    st.rerun()
    else:
        st.info("Chưa có trẻ nào. Thêm trẻ mới ở trên!")
    
    if st.session_state.tre_hien_tai:
        st.divider()
        st.success(f"✅ Đang chọn: **{st.session_state.tre_hien_tai['ten']}**")

# ===================== NỘI DUNG CHÍNH =====================
tab1, tab2, tab3 = st.tabs(["🔍 Sàng lọc phát triển", "📝 Soạn giáo án", "🎮 Trò chơi học tập"])

# ========== TAB 1: SÀNG LỌC PHÁT TRIỂN ==========
with tab1:
    st.header("🔍 Bảng sàng lọc dấu hiệu phát triển trẻ mầm non")
    
    if st.session_state.tre_hien_tai:
        tre = st.session_state.tre_hien_tai
        st.info(f"""
        👶 **Đang sàng lọc cho:** {tre.get('ten', 'Chưa có tên')}
        📅 **Ngày sinh:** {tre.get('ngay_sinh', 'Chưa có thông tin')}
        🎂 **Nhóm độ tuổi:** {tre.get('tuoi', 'Chưa xác định')}
        """)
        nhom_tuoi_sang_loc = tre['tuoi']
    else:
        st.warning("⚠️ Vui lòng chọn trẻ từ danh sách bên trái để sàng lọc chính xác hơn!")
        danh_sach_tuoi = list(DU_LIEU_SANG_LOC.keys())
        nhom_tuoi_sang_loc = st.selectbox(
            "Chọn nhóm độ tuổi cần sàng lọc:",
            danh_sach_tuoi,
            index=1
        )
    
    st.markdown("---")
    
    # Lấy dữ liệu sàng lọc
    if nhom_tuoi_sang_loc in DU_LIEU_SANG_LOC:
        du_lieu = DU_LIEU_SANG_LOC[nhom_tuoi_sang_loc]
        ket_qua = {}
        tong_dung = 0
        tong_cau = 0
        
        for nhom_cau, danh_sach_cau in du_lieu.items():
            st.subheader(f"📌 {nhom_cau}")
            ket_qua[nhom_cau] = []
            for cau, mac_dinh in danh_sach_cau:
                value = st.checkbox(cau, value=mac_dinh, key=f"{nhom_tuoi_sang_loc}_{nhom_cau}_{cau}")
                ket_qua[nhom_cau].append((cau, value))
                tong_cau += 1
                if value:
                    tong_dung += 1
            st.divider()
        
        # Lưu kết quả
        st.session_state.ket_qua_sang_loc = ket_qua
        
        # Tóm tắt kết quả
        ty_le = int((tong_dung / tong_cau * 100)) if tong_cau > 0 else 0
        st.subheader("📊 Tóm tắt kết quả")
        st.info(f"Tổng số tiêu chí: **{tong_cau}** | Đạt: **{tong_dung}** | Chưa đạt: **{tong_cau - tong_dung}** | Tỷ lệ đạt: **{ty_le}%**")
        
        # Nhận xét
        if ty_le >= 80:
            st.success("✅ Trẻ phát triển tốt trong các lĩnh vực được đánh giá!")
        elif ty_le >= 50:
            st.warning("⚠️ Trẻ cần chú ý và hỗ trợ thêm một số lĩnh vực!")
        else:
            st.error("🔴 Nên tham khảo ý kiến chuyên gia để có sự hỗ trợ phù hợp cho trẻ!")
        
        # Nút lưu kết quả
        if st.button("💾 Lưu kết quả sàng lọc"):
            st.success("✅ Đã lưu kết quả sàng lọc thành công!")

# ========== TAB 2: SOẠN GIÁO ÁN ==========
with tab2:
    st.header("📝 Soạn Giáo Án Đổi Mới")
    
    tre_hien_tai = st.session_state.tre_hien_tai
    ket_qua = st.session_state.ket_qua_sang_loc
    
    thong_tin_tre = ""
    goi_y_noi_dung = ""
    if tre_hien_tai:
        thong_tin_tre = f"- Tên trẻ: {tre_hien_tai['ten']}\n- Nhóm độ tuổi: {tre_hien_tai['tuoi']}\n- Ngày đánh giá: {datetime.now().strftime('%d/%m/%Y')}"
        
        # Tạo gợi ý dựa trên kết quả sàng lọc
        if ket_qua:
            chua_dat = []
            for nhom, danh_sach in ket_qua.items():
                for cau, dat in danh_sach:
                    if not dat:
                        chua_dat.append(f"- {nhom}: {cau}")
            if chua_dat:
                goi_y_noi_dung = "📌 Gợi ý nội dung trọng tâm dựa trên kết quả sàng lọc:\n" + "\n".join(chua_dat)
            else:
                goi_y_noi_dung = "✅ Trẻ phát triển tốt, duy trì các hoạt động hiện tại và phát triển nâng cao hơn!"
        else:
            goi_y_noi_dung = "Chưa có kết quả sàng lọc. Hoàn thành sàng lọc trước để có gợi ý nội dung phù hợp!"
    
    st.markdown(f"### Thông tin trẻ\n{thong_tin_tre if tre_hien_tai else 'Chưa chọn trẻ'}")
    if tre_hien_tai:
        st.info(goi_y_noi_dung)
    st.divider()
    
    # Form soạn giáo án
    chu_de = st.text_input("Chủ đề hoạt động:")
    muc_tieu = st.text_area("Mục tiêu (Kiến thức - Kỹ năng - Thái độ):", height=100)
    chuan_bi = st.text_area("Chuẩn bị (Đồ dùng - Không gian):", height=80)
    hoat_dong_chinh = st.text_area("Nội dung hoạt động chính (Các bước thực hiện):", height=150)
    hoat_dong_keo_dai = st.text_area("Hoạt động kéo dài & Ghi chú:", height=80)
    
    # Tạo nội dung giáo án
    noi_dung_giao_an = ""
    if chu_de or muc_tieu:
        noi_dung_giao_an = f"""
==================================================================
                    GIÁO ÁN HOẠT ĐỘNG MẦM NON
==================================================================

👶 Thông tin trẻ
{thong_tin_tre if tre_hien_tai else '- Chưa chọn trẻ'}

📌 Gợi ý từ kết quả sàng lọc
{goi_y_noi_dung if tre_hien_tai else '- Hoàn thành sàng lọc để nhận gợi ý nội dung phù hợp'}

==================================================================
📖 CHỦ ĐỀ: {chu_de or '(Chưa nhập chủ đề)'}

🎯 MỤC TIÊU
{muc_tieu or '(Chưa nhập mục tiêu)'}

📦 CHUẨN BỊ
{chuan_bi or '(Chưa nhập nội dung chuẩn bị)'}

📝 NỘI DUNG HOẠT ĐỘNG
{hoat_dong_chinh or '(Chưa nhập nội dung hoạt động)'}

⏳ HOẠT ĐỘNG KÉO DÀI & GHI CHÚ
{hoat_dong_keo_dai or '(Chưa nhập nội dung kéo dài)'}

==================================================================
Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Ứng dụng Trợ lý Giáo Viên Mầm Non
==================================================================
        """
    
    st.divider()
    st.subheader("Xem trước giáo án")
    st.code(noi_dung_giao_an, language=None)
    
    # Tải về máy
    col1, col2 = st.columns(2)
    with col1:
        if noi_dung_giao_an.strip() and st.download_button(
            label="💾 Tải giáo án về máy (.txt)",
            data=noi_dung_giao_an.encode('utf-8'),
            file_name=f"GiaoAn_{chu_de or 'ChuaDe'}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        ):
            st.success("✅ Giáo án đã được tải về máy!")
    with col2:
        if st.button("🖨️ In/Xem toàn màn hình"):
            st.info("👉 Nhấn Ctrl+P (hoặc Cmd+P trên Mac) để in tài liệu")

# ========== TAB 3: TRÒ CHƠI HỌC TẬP ==========
with tab3:
    st.header("🎮 Tạo Trò Chơi Học Tập")
    
    tre_hien_tai = st.session_state.tre_hien_tai
    if tre_hien_tai:
        st.info(f"👶 Đang tạo trò chơi cho: **{tre_hien_tai['ten']}** — Nhóm {tre_hien_tai['tuoi']}")
    else:
        st.warning("⚠️ Chọn trẻ bên trái để nhận gợi ý trò chơi phù hợp độ tuổi!")
    
    st.divider()
    
    loai_tro_choi = st.selectbox(
        "Chọn loại trò chơi:",
        ["Nhận biết thế giới xung quanh", "Phát triển ngôn ngữ", "Phát triển toán học sớm",
         "Phát triển thể chất", "Kỹ năng xã hội", "Sáng tạo nghệ thuật"]
    )
    
    noi_dung_tro_choi = st.text_area("Nội dung & Quy tắc trò chơi:", height=120)
    muc_tieu_tro_choi = st.text_area("Mục tiêu trò chơi:", height=80)
    cach_thuc_choi = st.text_area("Cách thực hiện & Lưu ý an toàn:", height=80)
    
    # Tạo nội dung hoàn chỉnh
    noi_dung_hoan_chinh = f"""
==================================================================
                TRÒ CHƠI HỌC TẬP MẦM NON
==================================================================

👶 Thông tin
- Trẻ: {tre_hien_tai['ten'] if tre_hien_tai else 'Nhiều trẻ'}
- Nhóm tuổi: {tre_hien_tai['tuoi'] if tre_hien_tai else 'Tất cả nhóm tuổi'}
- Ngày tạo: {datetime.now().strftime('%d/%m/%Y')}

🎮 Loại trò chơi: {loai_tro_choi}

🎯 Mục tiêu
{muc_tieu_tro_choi or '(Chưa nhập mục tiêu)'}

📝 Nội dung & Quy tắc
{noi_dung_tro_choi or '(Chưa nhập nội dung)'}

💡 Cách thực hiện & Lưu ý
{cach_thuc_choi or '(Chưa nhập hướng dẫn)'}

==================================================================
Ứng dụng Trợ lý Giáo Viên Mầm Non
==================================================================
    """
    
    st.divider()
    st.subheader("Xem trước trò chơi")
    st.code(noi_dung_hoan_chinh, language=None)
    
    # Tải về máy
    if noi_dung_tro_choi.strip() and st.download_button(
        label="💾 Tải trò chơi về máy (.txt)",
        data=noi_dung_hoan_chinh.encode('utf-8'),
        file_name=f"TroChoi_{loai_tro_choi.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    ):
        st.success("✅ Trò chơi đã được tải về máy!")

# ===================== CHÂN TRANG =====================
st.divider()
st.markdown("💡 **Lưu ý:** Dữ liệu được lưu tạm trong phiên làm việc. Tải tệp về máy để lưu trữ vĩnh viễn nhé!")
