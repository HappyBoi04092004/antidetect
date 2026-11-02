# Camoufox Antidetect Studio & Auto-Post Manager 🦊

Hệ thống quản lý trình duyệt Antidetect Browser chuyên nghiệp (Giao diện chuẩn phong cách GPM-Login Pro) tích hợp lõi vân tay **Camoufox (C++ Firefox Engine)**, tự động đăng nhập TikTok thông minh qua **OAuth2 Mail OTP (DongVanFB)** và hệ thống quản lý đăng bài, reup đa nền tảng (TikTok, YouTube Shorts, Reels, X, Lemon8).

---

## 🌟 Tính Năng Nổi Bật

### 1. 🛡️ Lõi Trình Duyệt Antidetect Camoufox
- Giả lập vân tay phần cứng chuyên sâu: Canvas noise, AudioContext, WebGL vendor/renderer, WebRTC IP leak protection.
- Tự động đồng bộ IP GeoIP (Timezone, Locale, Geolocation) theo vị trí của Proxy.
- Quản lý cookie và session tách biệt hoàn toàn cho từng profile.

### 2. 🖥️ Giao Diện Quản Lý Chuẩn GPM-Login Pro
- Bảng quản lý dạng spreadsheet trực quan, hiển thị STT, Tên profile, Nhóm, Proxy IP:Port, Trạng thái (Đang chạy / Đã tắt / Lỗi).
- Bộ lọc theo nhóm (`Tất Cả Nhóm`, phân loại theo thị trường US/UK/FR/VN...).
- Ô tìm kiếm nhanh đa trường: tìm theo tên profile, IP proxy, email hoặc ID tài khoản.
- Tác vụ hàng loạt (Batch Actions): Chọn nhiều profile để `Chạy Đồng Loạt`, `Dừng`, `Check Live Proxy`, `Xóa`.
- Hỗ trợ Chuyển đổi giao diện Sáng / Tối (Light & Dark Mode).
- Thanh trạng thái thống kê thời gian thực (Tổng profiles, Đang chạy, Đã chọn, Phiên bản Engine).

### 3. 🔐 Tự Động Đăng Nhập TikTok & Lấy OTP OAuth2 (DongVanFB)
- Tự động điền tài khoản, mật khẩu, xác thực người dùng.
- Tự động kết nối API `https://docs.dongvanfb.net/utils/get-code-mail-with-oauth2-token` để lấy mã OTP email trực tiếp theo định dạng:
  ```text
  username|password|email|passmail|refreshToken|clientId|mailBackup
  ```
- Tự động điền mã xác nhận và hoàn tất đăng nhập không cần can thiệp thủ công.

### 4. 🎬 Studio Quản Lý & Tự Động Đăng Bài Đa Nền Tảng
- Tự động tải video từ Douyin / TikTok / YouTube Shorts không watermark.
- AI SEO Assistant (Gemini) tối ưu hóa tiêu đề, mô tả và hashtag viral theo chủ đề.
- Chèn nhạc nền bản quyền an toàn (Safe BGM), biến đổi MD5 / lật khung hình tránh bản quyền.
- Lên lịch đăng bài tự động, quản lý hàng đợi và báo cáo kết quả qua Telegram Bot.

### 5. 🪟 Sẵn Sàng Cho macOS & Windows
- macOS: Nhấp đúp chạy ngay qua file `Chay_Ung_Dung.command`.
- Windows: Thư mục `Camoufox_Antidetect_Windows` kèm sẵn script cài đặt `Cai_Dat_Windows.bat`, khởi chạy `Chay_App_Windows.bat` và đóng gói file `.exe` bằng `Dong_Goi_EXE.bat`.

---

## 🚀 Cài Đặt & Khởi Chạy

### Yêu Cầu Hệ Thống
- Python 3.10 trở lên.
- Đã cài đặt FFmpeg (nếu sử dụng tính năng xử lý video reup).

### Trên macOS / Linux
```bash
# 1. Clone repository
git clone git@github.com:vutrunquan/antidetect.git
cd antidetect

# 2. Tạo môi trường ảo
python3 -m venv .venv
source .venv/bin/activate

# 3. Cài đặt thư viện
pip install -r requirements.txt
camoufox fetch

# 4. Chạy ứng dụng
python app.py
```

### Trên Windows
1. Tải về hoặc mở thư mục `Camoufox_Antidetect_Windows`.
2. Chạy `Cai_Dat_Windows.bat` (tự động cài đặt thư viện và tải browser engine).
3. Chạy `Chay_App_Windows.bat` để mở giao diện quản lý.

---

## 📁 Cấu Trúc Dự Án

```text
├── app.py                      # Server backend & Desktop GUI WebView
├── auto_login.py               # Module tự động đăng nhập TikTok & giải mã OTP DongVanFB
├── browser_runner.py           # Quản lý vòng đời khởi chạy Camoufox antidetect
├── profile_manager.py          # Quản lý danh sách profile, nhóm và cấu hình
├── post_manager.py             # Studio tự động tải, render và đăng bài đa nền tảng
├── platform_utils.py           # Tương tác giao diện đăng tải các nền tảng mạng xã hội
├── ai_seo_helper.py            # Tích hợp AI tạo caption, tiêu đề, hashtag viral
├── telegram_controller.py      # Điều khiển bot từ xa qua Telegram
├── requirements.txt            # Danh sách thư viện Python cần thiết
├── ui/
│   └── index.html              # Giao diện GPM-Login Pro (HTML5/CSS3/Vanilla JS)
├── Camoufox_Antidetect_Windows/ # Bản đóng gói dành riêng cho Windows
└── profiles.example.json       # File mẫu cấu hình profile
```

---

## 🔒 Bảo Mật (Security & Privacy)
- Thư mục `profiles/` (dữ liệu phiên duyệt web, cookie, local storage) và file cấu hình `profiles.json` được loại trừ trong `.gitignore` để đảm bảo tuyệt đối không rò rỉ thông tin cá nhân hay tài khoản.
- Không chia sẻ các file chứa `refreshToken`, `password` hoặc `proxy` lên repository công khai.

---

## 📄 License
Phát triển và bảo trì bởi [vutrunquan](https://github.com/vutrunquan).
Giấy phép: MIT License.

