# Hướng Dẫn Sử Dụng Camoufox Antidetect & Auto Studio Trên Windows

Chào mừng bạn đến với phiên bản **Camoufox Antidetect & Auto Studio dành cho Windows**!
Hệ thống tích hợp toàn diện: Trình duyệt Antidetect bảo mật Camoufox + Tự động đăng bài TikTok Studio / YouTube Shorts + Trợ lý AI SEO Gemini + Tự động vượt 2FA email DongVanFB.

---

## 1. Yêu cầu ban đầu trên máy Windows
1. Máy tính đã cài đặt **Python 3.10 trở lên** (tải từ [python.org](https://www.python.org/downloads/)).
   > ⚠️ **LƯU Ý QUAN TRỌNG KHI CÀI PYTHON:** Ở màn hình cài đặt đầu tiên, nhớ tích vào ô vuông **"Add python.exe to PATH"**!
2. *(Tùy chọn)* Nếu bạn sử dụng tính năng **Upscale 4K & Lách bản quyền bằng FFmpeg**:
   - Bạn chỉ cần tải `ffmpeg.exe` và `ffprobe.exe` đặt vào thư mục `bin\` trong thư mục này, hoặc cài qua lệnh:
     `winget install Gyan.FFmpeg`

---

## 2. Cách Cài Đặt (Chỉ làm 1 lần duy nhất)
1. Giải nén thư mục này ra vị trí bất kỳ (ví dụ: màn hình Desktop hoặc ổ đĩa `D:\`).
2. Nhấp đúp chuột vào file:
   👉 **`Cai_Dat_Windows.bat`**
3. Chương trình sẽ tự động:
   - Tạo môi trường ảo độc lập `.venv`.
   - Cài đặt đầy đủ các thư viện phụ thuộc (`camoufox`, `pywebview`, `yt-dlp`, `google-genai`, `requests`...).
   - Tự động tải bản build trình duyệt Firefox Windows x64 chống phát hiện bot và mô hình fingerprint.
4. Khi màn hình hiện thông báo **"CÀI ĐẶT THÀNH CÔNG"**, bấm phím bất kỳ để kết thúc.

---

## 3. Cách Mở Ứng Dụng Hàng Ngày
* Sau khi đã cài đặt xong, bạn chỉ cần nhấp đúp chuột vào file:
  👉 **`Chay_App_Windows.bat`**
* Ứng dụng Desktop hiện đại sẽ mở lên mượt mà (sử dụng Microsoft Edge WebView2 có sẵn trên Windows 10/11).

---

## 4. Các Tính Năng Đột Phá Đã Tích Hợp
1. **Quản Lý Profiles Antidetect**:
   - Tạo, sửa, xóa, nhân bản (clone) tài khoản không giới hạn.
   - Hỗ trợ mọi định dạng Proxy: `ip:port:user:pass` với nút kiểm tra IP & Quốc gia tức thì.
   - Cơ chế giả lập phần cứng: Canvas Noise, tắt WebRTC, Humanize di chuyển chuột tự nhiên.
2. **Auto-Login 1-Click (DongVanFB API)**:
   - Tự điền chuỗi tài khoản: `username|password|email|passmail|refreshToken|clientId|mailBackup`.
   - Tự nhận diện và vượt qua bước xác minh danh tính IDV Email của TikTok bằng cách gọi API DongVanFB lấy mã OTP 6 số tự động.
3. **Đăng Video & Trợ Lý AI SEO (Gemini)**:
   - Chọn video từ máy tính với hộp thoại chọn file native.
   - Nhấn 1 nút gọi Gemini AI tạo tiêu đề giật tít (<90 ký tự), câu hook mở đầu, mô tả SEO và 10-15 hashtags chuẩn thuật toán theo từng vùng VPN (VN, US, MX, ES, FR, DE...).
   - Upscale 4K dọc (2160x3840) và đổi mã băm khung hình chống reup.
   - Tự động hóa đăng bài lên TikTok Studio qua Camoufox:
     - Quét Content Check Lite bản quyền âm thanh 2 tầng.
     - Tự mix nhạc nền sạch (Safe BGM) nếu dính bản quyền và bấm Thay thế file.
     - Tự lưu Bản Nháp (Drafts) an toàn nếu quét lại vẫn dính cảnh báo.
   - Tự động hóa đăng lên YouTube Shorts (YouTube Studio): Chọn không dành cho trẻ em, đặt công khai và lấy link video.
4. **Quét Kênh Tự Động (Auto Scanner)**:
   - Thêm danh sách link YouTube Shorts đối thủ.
   - Tự động tải về khi có video mới, lách bản quyền và đăng chéo sang TikTok & YouTube theo chu kỳ cài đặt.
5. **Nhật Ký Thời Gian Thực (Live Execution Logs)**:
   - Khung console trực quan ở chân ứng dụng, theo dõi từng bước nạp file, quét bản quyền và đăng bài.
6. **Báo Cáo Telegram Tương Tác**:
   - Gửi báo cáo kèm nút bấm [🚀 Đăng ngay bản nháp] hoặc [🗑️ Xóa video] trực tiếp trên Telegram.
