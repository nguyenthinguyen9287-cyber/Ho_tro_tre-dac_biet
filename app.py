import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ==================== CẤU HÌNH KHÓA API ====================
API_KEY ="AQ.Ab8RN6LtXF8dfURCvlARItSSBGyW9haUrfBG_TNcKVtoP7Nkhg"
if API_KEY:
    genai.configure(api_key=API_KEY)

# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(
    page_title="Hỗ Trợ Trẻ Mầm Non - Phát Hiện & Can Thiệp Sớm",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== KHỞI TẠO DỮ LIỆU ====================
if 'danh_sach_tre' not in st.session_state:
    st.session_state.danh_sach_tre = []
if 'tre_hien_tai' not in st.session_state:
    st.session_state.tre_hien_tai = None
if 'lich_su_danh_gia' not in st.session_state:
    st.session_state.lich_su_danh_gia = []

# ==================== DỮ LIỆU CÂU HỎI ASQ-3 (6 CÂU/LĨNH VỰC) ====================
cau_hoi_asq3 = {
    "Giao tiếp": [
        {"cau": "Trẻ chỉ vào đồ vật khi muốn bạn xem?", "mo_ta": "Chỉ để chia sẻ sự chú ý, không phải để yêu cầu"},
        {"cau": "Trẻ làm theo 1 bước yêu cầu đơn giản mà không cần cử chỉ chỉ dẫn?", "mo_ta": "Ví dụ: 'Đưa cho tôi cái cốc'"},
        {"cau": "Trẻ nói có từ 2–3 từ trở lên?", "mo_ta": "Ví dụ: 'Mẹ ơi, bóng'"},
        {"cau": "Trẻ gọi tên đồ vật hoặc người quen chính xác?", "mo_ta": "Không phải chỉ chỉ vào thôi"},
        {"cau": "Trẻ lặp bập hoặc cố gắng giao tiếp với bạn bằng âm thanh/ngôn ngữ?", "mo_ta": "Chủ động giao tiếp, không chỉ trả lời"},
        {"cau": "Trẻ hiểu ý nghĩa của các từ thông dụng hàng ngày?", "mo_ta": "Ví dụ: ăn, ngủ, đi, cầm..."}
    ],
    "Vận động tinh": [
        {"cau": "Trẻ dùng ngón tay cái và ngón trỏ nhặt đồ vật nhỏ?", "mo_ta": "Nhặt chút bánh, hạt nhỏ bằng 2 ngón tay"},
        {"cau": "Trẻ lật từng trang sách?", "mo_ta": "Không lật nhiều trang cùng lúc"},
        {"cau": "Trẻ vẽ nguệch ngoạc khi cầm bút chì?", "mo_ta": "Tự cầm và vẽ được vài nét"},
        {"cau": "Trẻ xếp được 2 khối gỗ chồng lên nhau?", "mo_ta": "Không bị đổ ngay sau đó"},
        {"cau": "Trẻ lấy đồ vật từ trong hộp/bao bì?", "mo_ta": "Tự mở hoặc thò tay lấy ra được"},
        {"cau": "Trẻ xoay cổ tay để đưa đồ cho người khác?", "mo_ta": "Thay đổi hướng cầm đồ vật phù hợp"}
    ],
    "Vận động thô": [
        {"cau": "Trẻ đi được mà không cần nắm tay hay giữ vật?", "mo_ta": "Đi thẳng vài bước không ngã liên tục"},
        {"cau": "Trẻ ngồi vững không cần tựa lưng?", "mo_ta": "Ngồi trên sàn được ít nhất 10 phút"},
        {"cau": "Trẻ nhấc chân lên bước qua vật thấp?", "mo_ta": "Bước qua gối, dây điện... mà không vấp ngã"},
        {"cau": "Trẻ ngồi xuống từ tư thế đứng?", "mo_ta": "Không ngã hay té xuống"},
        {"cau": "Trẻ chạy được vài bước?", "mo_ta": "Chưa cần nhanh nhưng không bị vấp thường xuyên"},
        {"cau": "Trẻ leo lên ghế thấp hoặc bậc thang 1 bậc?", "mo_ta": "Tự chủ động leo lên an toàn"}
    ],
    "Giải quyết vấn đề": [
        {"cau": "Trẻ tìm vật khi bạn giấu nó dưới khăn?", "mo_ta": "Biết lật khăn lên để lấy vật"},
        {"cau": "Trẻ dùng thử cách khác khi cách cũ không được?", "mo_ta": "Ví dụ: kéo thay vì đẩy hộp đồ nặng"},
        {"cau": "Trẻ bắt chước hành động đơn giản của bạn?", "mo_ta": "Vỗ tay, lắc đầu, cười... theo bạn"},
        {"cau": "Trẻ đưa cho bạn đồ khi bạn giơ tay?", "mo_ta": "Hiểu yêu cầu và hợp tác"},
        {"cau": "Trẻ chú ý đến hình ảnh trong gương?", "mo_ta": "Nhìn, chạm hoặc mỉm cười với ảnh mình"},
        {"cau": "Trẻ chơi với đồ vật theo chức năng cơ bản?", "mo_ta": "Ví dụ: cầm ly uống, cầm điện thoại nghe"}
    ],
    "Cá nhân - Xã hội": [
        {"cau": "Trẻ chơi cùng bạn được một lát?", "mo_ta": "Chơi cạnh hoặc chung đồ với trẻ khác"},
        {"cau": "Trẻ tự ăn được một phần bữa ăn bằng tay?", "mo_ta": "Cầm miếng bánh, quả... bỏ vào miệng"},
        {"cau": "Trẻ thể hiện tình cảm với người thân?", "mo_ta": "Ôm, hôn, mỉm cười khi gặp gia đình"},
        {"cau": "Trẻ đáp ứng khi gọi tên mình?", "mo_ta": "Ngẩng đầu/quay lại trong vòng vài giây"},
        {"cau": "Trẻ nói 'không' hoặc lắc đầu khi không muốn?", "mo_ta": "Thể hiện sự từ chối một cách rõ ràng"},
        {"cau": "Trẻ giúp đỡ những việc đơn giản?", "mo_ta": "Cất đồ chơi, đưa vật khi bạn yêu cầu"}
    ]
}

# ==================== CÂU HỎI SÀNG LỌC RỐI LOẠN PHỔ TỰ KỶ ====================
cau_hoi_tu_ky = [
    {"cau": "Trẻ có nhìn thẳng vào mắt người nói chuyện không?", "giai_thich": "Trẻ thường né tránh ánh mắt, nhìn ra hướng khác"},
    {"cau": "Trẻ có mỉm cười đáp lại khi bạn cười với trẻ không?", "giai_thich": "Không biểu hiện cảm xúc, ít phản ứng với nét mặt người khác"},
    {"cau": "Trẻ có chỉ vào đồ vật để chia sẻ không?", "giai_thich": "Chỉ dùng tay lấy trực tiếp, không chia sẻ sự chú ý"},
    {"cau": "Trẻ có bắt chước hành động/âm thanh của người khác không?", "giai_thich": "Ít bắt chước, lặp lại hành động giống hệt nhau"},
    {"cau": "Trẻ có quan tâm đến trẻ khác cùng độ tuổi không?", "giai_thich": "Chơi một mình, không chú ý đến bạn xung quanh"},
    {"cau": "Trẻ có lặp lại một hành động giống hệt nhiều lần không?", "giai_thich": "Xoay vật, lắc người, xếp đồ theo một thứ tự cố định"},
    {"cau": "Trẻ có phản ứng bất thường khi thay đổi thói quen không?", "giai_thich": "Phản ứng quá mạnh, khóc, la hét khi thay đổi lịch trình"},
    {"cau": "Trẻ có dùng ngôn ngữ để giao tiếp hai chiều không?", "giai_thich": "Nói lặp lại lời người khác, nói một mình, không hội thoại"}
]

# ==================== CÂU HỎI SÀNG LỌC KHẾT TẬT PHÁT TRIỂN ====================
cau_hoi_khuyet_tat = [
    {"cau": "Trẻ có phản ứng khi có tiếng động xung quanh không?", "giai_thich": "Không quay đầu khi gọi tên, không phản ứng tiếng to"},
    {"cau": "Trẻ có nhìn theo vật chuyển động không?", "giai_thich": "Không theo dõi bằng mắt, nhìn vào khoảng không"},
    {"cau": "Trẻ có cầm nắm đồ vật theo đúng cách không?", "giai_thich": "Bỏ lơ, không nắm được, cầm bất thường"},
    {"cau": "Trẻ có tự ngồi được khi được hỗ trợ không?", "giai_thich": "Thân người mềm nhũn hoặc cứng đờ, không giữ thăng bằng"},
    {"cau": "Trẻ có cố gắng giao tiếp bằng âm thanh không?", "giai_thich": "Không phát ra âm thanh, không có biểu cảm khi giao tiếp"},
    {"cau": "Trẻ có thực hiện được các động tác đơn giản so với độ tuổi không?", "giai_thich": "Chậm hơn hẳn bạn cùng trang lứa, không tiến bộ theo thời gian"}
]

# ==================== 3 MẪU KẾ HOẠCH CÁ NHÂN ====================
mau_ke_hoach = {
    "Theo dõi thường xuyên": {
        "muc_tieu": "Theo dõi sát sao tiến độ phát triển, tạo môi trường hỗ trợ phù hợp, đảm bảo trẻ theo kịp các mốc phát triển cơ bản.",
        "thoi_gian": "3 tháng",
        "noi_dung_chinh": [
            "Quan sát, ghi nhận biểu hiện hàng ngày tại lớp và tại nhà",
            "Tổ chức hoạt động theo nhóm nhỏ, kèm cặp với bạn tốt",
            "Lặp lại yêu cầu đơn giản, dùng hình ảnh minh họa",
            "Kết hợp phối hợp với gia đình theo dõi tiến độ",
            "Đánh giá lại sau 3 tháng để điều chỉnh kế hoạch"
        ],
        "nguoi_thuc_hien": "Giáo viên chủ nhiệm + Phụ huynh",
        "cach_danh_gia": "Quan sát hàng ngày, ghi chép tiến độ, trao đổi với gia đình hàng tuần"
    },
    "Hỗ trợ can thiệp tại lớp & nhà": {
        "muc_tieu": "Xây dựng kế hoạch hỗ trợ có mục tiêu cụ thể, bám sát trình độ hiện tại của trẻ, từng bước nâng cao kỹ năng giao tiếp, xã hội và tự phục vụ.",
        "thoi_gian": "6 tháng",
        "noi_dung_chinh": [
            "Xác định kỹ năng ưu tiên cần rèn luyện: giao tiếp, ngôn ngữ, vận động, tự phục vụ",
            "Chia nhỏ từng kỹ năng thành các bước dễ thực hiện, củng cố bằng phần thưởng tích cực",
            "Thực hiện bài tập theo kế hoạch: 20–30 phút/ngày tại lớp + lặp lại tại nhà",
            "Sử dụng hình ảnh, thẻ giao tiếp, mô hình hành vi",
            "Tổ chức hoạt động chơi cùng bạn để rèn kỹ năng xã hội",
            "Trao đổi với gia đình hàng tuần, điều chỉnh nội dung phù hợp"
        ],
        "nguoi_thuc_hien": "Giáo viên chuyên trách + Phụ huynh + Giáo viên chủ nhiệm",
        "cach_danh_gia": "Bảng kiểm hàng ngày, báo cáo tiến độ mỗi tháng, đánh giá lại sau 3 tháng"
    },
    "Can thiệp chuyên sâu": {
        "muc_tieu": "Phối hợp đa ngành: giáo dục, y tế, tâm lý — xây dựng chương trình can thiệp cá nhân hóa chuyên sâu, tối đa hóa tiềm năng phát triển của trẻ.",
        "thoi_gian": "12 tháng",
        "noi_dung_chinh": [
            "Tham khảo ý kiến bác sĩ, chuyên gia tâm lý, trị liệu ngôn ngữ, vận động",
            "Xác định rõ mức độ và lĩnh vực cần can thiệp chính",
            "Xây dựng chương trình cá nhân hóa theo PEP-R/ASQ: chia nhỏ mục tiêu thành từng bước cụ thể",
            "Thực hiện can thiệp có hướng dẫn chuyên gia: 30–45 phút/buổi, 3–5 buổi/tuần",
            "Phối hợp chặt chẽ giữa nhà trường, gia đình và trung tâm can thiệp",
            "Theo dõi tiến độ bằng phiếu đánh giá chuẩn mỗi tháng, điều chỉnh kế hoạch kịp thời"
        ],
        "nguoi_thuc_hien": "Chuyên gia can thiệp + Giáo viên chuyên trách + Phụ huynh + Bác sĩ",
        "cach_danh_gia": "Đánh giá chuẩn mỗi tháng, báo cáo đa ngành mỗi quý, xem xét lại chương trình sau 6 tháng"
    }
}

# ==================== THƯ VIỆN HOẠT ĐỘNG ====================
thu_vien_hoat_dong = {
    "Ngôn ngữ & Giao tiếp": [
        {"ten": "100 từ đầu tiên", "muc_dich": "Xây dựng vốn từ vựng nền tảng hàng ngày", "cach_thuc_hien": "Nêu tên đồ vật trong cuộc sống, lặp lại nhiều lần, khuyến khích trẻ bắt chước; bắt đầu từ từ chỉ người thân, đồ ăn, đồ chơi quen thuộc", "thoi_gian": "5–10 phút, nhiều lần trong ngày"},
        {"ten": "Nói theo mô hình", "muc_dich": "Rèn kỹ năng lặp lại và tạo câu đơn giản", "cach_thuc_hien": "Nói câu ngắn gọn, chậm rãi → khuyến khích trẻ lặp; bắt đầu từ 2 từ → 3 từ theo khả năng của trẻ", "thoi_gian": "5–10 phút/lần"},
        {"ten": "Thẻ hình ảnh giao tiếp (AAC)", "muc_dich": "Hỗ trợ trẻ chưa nói được biểu đạt nhu cầu", "cach_thuc_hien": "In hình ảnh đồ ăn, đồ chơi, hành động → trẻ chỉ vào thẻ khi cần; dần dần kết hợp chỉ thẻ + nói từ", "thoi_gian": "Thường xuyên trong ngày"},
        {"ten": "Nghe và kể lại truyện ngắn theo tranh", "muc_dich": "Rèn hiểu nghe, ghi nhớ và diễn đạt", "cach_thuc_hien": "Dùng sách tranh ít chữ → đọc cho trẻ nghe → đặt câu hỏi đơn giản: 'Ai đây?', 'Làm gì vậy?'", "thoi_gian": "10–15 phút/lần"}
    ],
    "Vận động tinh & Tay": [
        {"ten": "Nhặt đồ vật nhỏ", "muc_dich": "Rèn kẹp ngón cái – ngón trỏ", "cach_thuc_hien": "Cho trẻ nhặt hạt lớn, miếng bánh, viên bi to vào hộp; giảm dần kích thước khi thành thạo", "thoi_gian": "5–8 phút/lần"},
        {"ten": "Xâu hạt, vòng lớn", "muc_dich": "Phối hợp tay – mắt, điều khiển lực tay", "cach_thuc_hien": "Dùng que và vòng nhựa to → hướng dẫn trẻ xâu vào que; khen thưởng khi thành công", "thoi_gian": "5–10 phút/lần"},
        {"ten": "Tô màu, vẽ nét đơn giản", "muc_dich": "Cầm bút, điều khiển nét vẽ", "cach_thuc_hien": "Bắt đầu tô tự do → tô trong khung rộng → vẽ nét thẳng, vòng tròn theo mẫu", "thoi_gian": "5–10 phút/lần"},
        {"ten": "Gấp, xé giấy; nhặt nắp chai", "muc_dich": "Rèn cơ tay, linh hoạt ngón tay", "cach_thuc_hien": "Xé giấy thành mảnh nhỏ → dán; mở nắp chai nhựa lớn → đóng lại", "thoi_gian": "5–10 phút/lần"}
    ],
    "Vận động thô": [
        {"ten": "Đi theo đường kẻ, vượt chướng ngại vật thấp", "muc_dich": "Thăng bằng, phối hợp chuyển động", "cach_thuc_hien": "Kẻ đường thẳng trên sàn → trẻ đi trên đường; đặt gối, hộp thấp → trẻ bước qua", "thoi_gian": "10–15 phút/lần"},
        {"ten": "Nhảy, chạy theo nhạc", "muc_dich": "Phối hợp toàn thân, phản xạ", "cach_thuc_hien": "Bật nhạc vui → hướng dẫn trẻ nhảy, vỗ tay, chạy chậm theo nhịp; khen thưởng khi tham gia", "thoi_gian": "10–15 phút/lần"},
        {"ten": "Leo cầu thang, lên xuống ghế", "muc_dich": "Phát triển cơ chân, tự tin chuyển động", "cach_thuc_hien": "Bắt đầu 1 bậc thang thấp → hỗ trợ dần giảm bớt; lên xuống ghế thấp giữ tay", "thoi_gian": "Theo dõi sát, thực hiện hàng ngày"}
    ],
    "Hành vi & Kỹ năng Xã hội": [
        {"ten": "Nhận biết cảm xúc qua hình ảnh", "muc_dich": "Nhận diện và biểu đạt cảm xúc", "cach_thuc_hien": "Chỉ vào mặt trong tranh → hỏi: 'Bạn ấy vui hay khóc?' → hướng dẫn trẻ chỉ hoặc nói", "thoi_gian": "5–10 phút/lần"},
        {"ten": "Chia sẻ & Luân phiên", "muc_dich": "Hợp tác, hiểu quy tắc chơi", "cach_thuc_hien": "Chơi cùng trẻ khác: 'Bạn chơi trước, rồi đến con' → khen khi trẻ đưa đồ cho bạn; lặp lại thường xuyên", "thoi_gian": "Thường xuyên trong ngày"},
        {"ten": "Tự phục vụ cơ bản", "muc_dich": "Tự lập, hình thành thói quen", "cach_thuc_hien": "Tự cầm muỗng ăn, tự cởi giày, cất đồ chơi sau chơi; chia nhỏ bước, hướng dẫn bằng cử chỉ + lời nói ngắn gọn", "thoi_gian": "Hàng ngày, kiên nhẫn hướng dẫn lại nhiều lần"},
        {"ten": "100 bài tập can thiệp hành vi tích cực", "muc_dich": "Thay thế hành vi không phù hợp bằng hành vi mong muốn", "cach_thuc_hien": "Quan sát ghi nhận nguyên nhân hành vi → dạy trẻ cách biểu đạt nhu cầu bằng lời/cử chỉ → khen thưởng ngay khi trẻ làm đúng; không trừng phạt hành vi sai", "thoi_gian": "Liên tục, bền bỉ hàng ngày"}
    ],
    "Phối hợp Gia đình": [
        {"ten": "Bài tập củng cố tại nhà", "muc_dich": "Nhất quán giữa trường và nhà", "cach_thuc_hien": "Giáo viên hướng dẫn bài tập cụ thể → phụ huynh thực hiện 15–20 phút/ngày → ghi nhận tiến độ vào sổ liên lạc", "thoi_gian": "Hàng ngày, trao đổi hàng tuần"},
        {"ten": "Cách nói & giao tiếp nhất quán", "muc_dich": "Trẻ dễ hiểu, không bối rối", "cach_thuc_hien": "Dùng cùng từ, cùng cách gọi đồ vật; cùng quy tắc: 'không' là không ở cả nhà và trường; lặp lại yêu cầu một cách bình tĩnh", "thoi_gian": "Liên tục mọi lúc"}
    ]
}

# ==================== TIÊU ĐỀ ====================
st.markdown("""
    <h1 style='text-align: center; color: #ff6b9d;'>🌸 Hỗ Trợ Trẻ Mầm Non - Phát Hiện & Can Thiệp Sớm</h1>
    <p style='text-align: center; color: #666;'>Bộ công cụ toàn diện: Đánh giá ASQ-3 • Sàng lọc • Kế hoạch cá nhân • Thư viện hoạt động</p>
    <hr style='border: 1px solid #ffd6e0;'>
""", unsafe_allow_html=True)

# ==================== THANH BÊN TRÁI ====================
with st.sidebar:
    st.header("👶 Thông tin trẻ")
    ten_tre = st.text_input("Tên trẻ:")
    ngay_sinh = st.date_input("Ngày sinh:")
    nhom_tuoi = st.selectbox("Nhóm độ tuổi:", [
        "18–24 tháng",
        "25–36 tháng"
    ])
    nguoi_danh_gia = st.text_input("Người đánh giá:")
    ghi_chu = st.text_area("Ghi chú / Đặc điểm cần lưu ý:")
    
    if st.button("💾 Lưu thông tin trẻ"):
        if ten_tre:
            tre_moi = {
                "ten": ten_tre,
                "ngay_sinh": ngay_sinh,
                "tuoi": nhom_tuoi,
                "nguoi_danh_gia": nguoi_danh_gia,
                "ngay_danh_gia": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "ghi_chu": ghi_chu
            }
            st.session_state.tre_hien_tai = tre_moi
            st.success(f"✅ Đã lưu: {ten_tre} — {nhom_tuoi}")
        else:
            st.warning("⚠️ Vui lòng nhập tên trẻ!")
    
    st.divider()
    st.subheader("📋 Chức năng chính")
    tab_chon = st.radio("Chọn chức năng:", [
        "📝 Đánh giá phát triển ASQ-3",
        "🔍 Sàng lọc sớm",
        "📄 Tạo kế hoạch cá nhân",
        "📚 Thư viện hoạt động",
        "📊 Lịch sử & Báo cáo"
    ])

# ==================== TAB 1: ĐÁNH GIÁ ASQ-3 ====================
if tab_chon == "📝 Đánh giá phát triển ASQ-3":
    if not st.session_state.tre_hien_tai:
        st.info("👈 Vui lòng nhập thông tin trẻ ở thanh bên trái trước khi đánh giá!")
    else:
        tre = st.session_state.tre_hien_tai
        st.subheader(f"📋 Đánh giá ASQ-3 cho: {tre['ten']} — {tre['tuoi']}")
        st.caption(f"Ngày: {tre['ngay_danh_gia']} | Người đánh giá: {tre['nguoi_danh_gia']}")
        
        tong_diem = {}
        for linh_vuc, danh_sach_cau in cau_hoi_asq3.items():
            st.markdown(f"### ✅ {linh_vuc} (6 câu)")
            st.caption("Trả lời dựa trên quan sát thực tế của trẻ trong 1–2 tháng qua:")
            
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
        
        if st.button("💾 Lưu kết quả ASQ-3"):
            ket_qua = {
                "loai": "ASQ-3",
                "ten_tre": tre["ten"],
                "tuoi": tre["tuoi"],
                "ngay": tre["ngay_danh_gia"],
                "nguoi_danh_gia": tre["nguoi_danh_gia"],
                "diem": tong_diem,
                "ghi_chu": tre["ghi_chu"]
            }
            st.session_state.lich_su_danh_gia.append(ket_qua)
            st.success("🎉 Đã lưu! Chuyển tab 'Tạo kế hoạch cá nhân' để xây dựng giải pháp hỗ trợ phù hợp.")

# ==================== TAB 2: SÀNG LỌC SỚM ====================
elif tab_chon == "🔍 Sàng lọc sớm":
    if not st.session_state.tre_hien_tai:
        st.info("👈 Vui lòng nhập thông tin trẻ ở thanh bên trái trước!")
    else:
        tre = st.session_state.tre_hien_tai
        st.subheader(f"🔍 Sàng lọc sớm cho: {tre['ten']}")
        
        loai_sang_loc = st.radio("Chọn loại sàng lọc:", [
            "Rối loạn phổ tự kỷ (8 câu)",
            "Khuyết tật phát triển (6 câu)"
        ])
        
        if loai_sang_loc == "Rối loạn phổ tự kỷ (8 câu)":
            st.warning("⚠️ Đây là công cụ sàng lọc ban đầu, **không phải công cụ chẩn đoán chính thức**. Nếu có dấu hiệu bất thường, hãy tham khảo chuyên gia!")
            ds_cau = cau_hoi_tu_ky
            so_cau_dung = 0
            
            for so_thu_tu, cau in enumerate(ds_cau, 1):
                st.markdown(f"**Câu {so_thu_tu}/8:** {cau['cau']}")
                st.caption(f"💡 Dấu hiệu cần chú ý: {cau['giai_thich']}")
                lua_chon = st.radio(
                    f"Trẻ có biểu hiện như mô tả không?",
                    options=["Không", "Đôi khi", "Thường xuyên"],
                    key=f"autism_{so_thu_tu}",
                    horizontal=True
                )
                if lua_chon in ["Đôi khi", "Thường xuyên"]:
                    so_cau_dung += 1
                st.divider()
            
            st.markdown("### 📊 Kết quả sàng lọc:")
            if so_cau_dung >= 5:
                st.error(f"🔴 {so_cau_dung}/8 câu — Có nhiều dấu hiệu cần tham khảo chuyên gia sớm!")
                st.markdown("""
                **Khuyến nghị:**
                • Tham khảo bác sĩ nhi khoa / trung tâm can thiệp sớm
                • Không tự kết luận, cần đánh giá chuẩn chuyên môn
                • Lập kế hoạch hỗ trợ cá nhân hóa cho trẻ
                """)
            elif 3 <= so_cau_dung < 5:
                st.warning(f"⚠️ {so_cau_dung}/8 câu — Cần theo dõi sát sao trong 1–2 tháng tới")
                st.markdown("""
                **Khuyến nghị:**
                • Quan sát thường xuyên hơn
                • Tăng tương tác, chơi cùng trẻ nhiều hơn
                • Đánh giá lại sau 1 tháng
                """)
            else:
                st.success(f"✅ {so_cau_dung}/8 câu — Chưa có dấu hiệu đáng lo ngại. Tiếp tục quan sát bình thường!")
        
        else:
            st.warning("⚠️ Công cụ này chỉ nhằm phát hiện sớm dấu hiệu chậm phát triển, không thay thế chẩn đoán y khoa!")
            ds_cau = cau_hoi_khuyet_tat
            so_cau_dung = 0
            
            for so_thu_tu, cau in enumerate(ds_cau, 1):
                st.markdown(f"**Câu {so_thu_tu}/6:** {cau['cau']}")
                st.caption(f"💡 Dấu hiệu bất thường: {cau['giai_thich']}")
                lua_chon = st.radio(
                    f"Trẻ có biểu hiện này không?",
                    options=["Không", "Có, nhưng ít", "Có, rõ ràng"],
                    key=f"khuyet_{so_thu_tu}",
                    horizontal=True
                )
                if lua_chon in ["Có, nhưng ít", "Có, rõ ràng"]:
                    so_cau_dung += 1
                st.divider()
            
            st.markdown("### 📊 Kết quả sàng lọc:")
            if so_cau_dung >= 4:
                st.error(f"🔴 {so_cau_dung}/6 câu — Khuyến nghị tham khảo bác sĩ sớm!")
                st.markdown("""
                **Khuyến nghị:**
                • Khám tai mũi họng, thính lực, thị lực
                • Tham khảo chuyên gia phát triển trẻ em
                • Xây dựng kế hoạch can thiệp sớm
                """)
            elif 2 <= so_cau_dung < 4:
                st.warning(f"⚠️ {so_cau_dung}/6 câu — Cần theo dõi và đánh giá lại sau 1 tháng")
            else:
                st.success(f"✅ {so_cau_dung}/6 câu — Tiếp tục theo dõi phát triển bình thường!")

# ==================== TAB 3: KẾ HOẠCH CÁ NHÂN ====================
elif tab_chon == "📄 Tạo kế hoạch cá nhân":
    if not st.session_state.tre_hien_tai:
        st.info("👈 Vui lòng nhập thông tin trẻ ở thanh bên trái trước!")
    else:
        tre = st.session_state.tre_hien_tai
        st.subheader(f"📄 Kế hoạch hỗ trợ cá nhân hóa: {tre['ten']}")
        
        muc_do = st.selectbox("Chọn mức độ hỗ trợ phù hợp:", list(mau_ke_hoach.keys()))
        
        ke_hoach = mau_ke_hoach[muc_do]
        
        st.markdown(f"### 📌 Mẫu: {muc_do}")
        st.markdown(f"**🎯 Mục tiêu:** {ke_hoach['muc_tieu']}")
        st.markdown(f"**⏱️ Thời gian:** {ke_hoach['thoi_gian']}")
        st.markdown(f"**👤 Người thực hiện:** {ke_hoach['nguoi_thuc_hien']}")
        
        st.markdown("### 📋 Nội dung chính:")
        for stt, nd in enumerate(ke_hoach["noi_dung_chinh"], 1):
            st.markdown(f"{stt}. {nd}")
        
        st.markdown("### 📝 Cách đánh giá & theo dõi:")
        st.info(ke_hoach["cach_danh_gia"])
        
        st.divider()
        st.markdown("### ✏️ Tùy chỉnh cho trẻ:")
        muc_tieu_rieng = st.text_area("Mục tiêu cụ thể trong tháng này:", height=100, placeholder="Ví dụ: Trẻ tự gọi tên khi được hỏi...")
        hoat_dong_rieng = st.text_area("Hoạt động ưu tiên thực hiện hàng ngày:", height=100, placeholder="Ví dụ: 10 phút lặp từ vựng quen thuộc sau bữa ăn...")
        phu_huynh_dong_thai = st.text_area("Điều phối với gia đình:", height=80, placeholder="Phụ huynh thực hiện bài tập lặp từ 10 phút tối...")
        
        if st.button("💾 Lưu kế hoạch này"):
            ke_hoach_hoan_chinh = {
                "loai": "KeHoachCaNhan",
                "ten_tre": tre["ten"],
                "muc_do": muc_do,
                "ngay_tao": datetime.now().strftime("%d/%m/%Y"),
                "muc_tieu_chung": ke_hoach["muc_tieu"],
                "muc_tieu_rieng": muc_tieu_rieng,
                "hoat_dong_rieng": hoat_dong_rieng,
                "phu_huynh_phoi_hop": phu_huynh_dong_thai,
                "thoi_gian": ke_hoach["thoi_gian"]
            }
            st.session_state.lich_su_danh_gia.append(ke_hoach_hoan_chinh)
            st.success("🎉 Đã lưu kế hoạch! Xem lại trong tab 'Lịch sử & Báo cáo'")
        
        st.divider()
        st.info("💡 **Lời khuyên:** Kế hoạch là hướng dẫn, không phải quy tắc cứng nhắc. Hãy điều chỉnh theo nhịp độ thực tế của trẻ, linh hoạt và kiên nhẫn!")

# ==================== TAB 4: THƯ VIỆN HOẠT ĐỘNG ====================
elif tab_chon == "📚 Thư viện hoạt động":
    st.subheader("📚 Kho thư viện hoạt động hỗ trợ phát triển")
    st.caption("Dựa trên tài liệu: PEP-R, 100 bài tập can thiệp, 100 từ đầu tiên, AAC, hướng dẫn can thiệp tại nhà")
    
    linh_vuc_chon = st.selectbox("Chọn lĩnh vực phát triển:", list(thu_vien_hoat_dong.keys()))
    
    ds_hoat_dong = thu_vien_hoat_dong[linh_vuc_chon]
    for so_thu_tu, hd in enumerate(ds_hoat_dong, 1):
        with st.expander(f"📌 {hd['ten']} — {hd['thoi_gian']}"):
            st.markdown(f"**🎯 Mục đích:** {hd['muc_dich']}")
            st.markdown(f"**📝 Cách thực hiện:** {hd['cach_thuc_hien']}")
            st.markdown(f"**⏱️ Thời gian:** {hd['thoi_gian']}")
    
    st.divider()
    st.markdown("### 💡 Lưu ý khi áp dụng:")
    st.markdown("""
    - Bắt đầu từ mức dễ nhất, không đòi hỏi trẻ quá sớm
    - Khen thưởng ngay khi trẻ cố gắng hoặc làm đúng
    - Lặp lại nhiều lần trong ngày, mỗi lần ngắn hơn hiệu quả hơn
    - Phối hợp với gia đình thực hiện cùng một cách
    - Thay đổi hoạt động khi trẻ mất hứng thú
    """)

# ==================== TAB 5: LỊCH SỬ & BÁO CÁO ====================
elif tab_chon == "📊 Lịch sử & Báo cáo":
    st.subheader("📊 Lịch sử theo dõi & Báo cáo")
    
    if not st.session_state.lich_su_danh_gia:
        st.info("Chưa có dữ liệu. Hoàn thành đánh giá hoặc tạo kế hoạch để lưu lại nhé!")
    else:
        st.write(f"Tổng số bản ghi: {len(st.session_state.lich_su_danh_gia)}")
        
        for chi_so, ban_ghi in enumerate(reversed(st.session_state.lich_su_danh_gia), 1):
            with st.expander(f"📅 {ban_ghi['ngay']} — {ban_ghi['ten_tre']}"):
                if ban_ghi.get("loai") == "ASQ-3":
                    st.markdown("**📋 Kết quả đánh giá ASQ-3:**")
                    for lv, diem in ban_ghi["diem"].items():
                        st.metric(label=lv, value=f"{diem}/60")
                elif ban_ghi.get("loai") == "KeHoachCaNhan":
                    st.markdown(f"**📄 Kế hoạch:** {ban_ghi['muc_do']}")
                    st.markdown(f"**Mục tiêu chung:** {ban_ghi['muc_tieu_chung']}")
                    if ban_ghi.get("muc_tieu_rieng"):
                        st.markdown(f"**Mục tiêu riêng:** {ban_ghi['muc_tieu_rieng']}")
                    if ban_ghi.get("hoat_dong_rieng"):
                        st.markdown(f"**Hoạt động:** {ban_ghi['hoat_dong_rieng']}")
                else:
                    st.json(ban_ghi)
        
        st.divider()
        if st.button("🗑️ Xóa toàn bộ lịch sử"):
            st.session_state.lich_su_danh_gia = []
            st.success("Đã xóa toàn bộ lịch sử!")
            st.rerun()
