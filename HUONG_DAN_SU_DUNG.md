# Hướng Dẫn Sử Dụng Camoufox (Anti-detect Browser)

## 1. Môi trường đã cài đặt sẵn
- Mã nguồn Camoufox đã được clone tại thư mục `camoufox/`.
- Môi trường ảo Python đã được khởi tạo tại `.venv/`.
- Bản build trình duyệt Camoufox (Firefox tùy biến C++ chống phát hiện bot), GeoIP database và model fingerprint đã được tải về đầy đủ thông qua `camoufox fetch`.

---

## 2. Kích hoạt môi trường (Virtual Environment)
Mỗi khi mở terminal mới tại thư mục `antidetect`, hãy chạy lệnh:
```bash
source .venv/bin/activate
```

---

## 3. Các ví dụ mẫu đã chuẩn bị

### Ví dụ 1: Chạy trình duyệt cơ bản (`demo_basic.py`)
Khởi chạy trình duyệt có giao diện (`headless=False`), tự động spoof thông tin thiết bị ngẫu nhiên và mở trang kiểm tra fingerprint:
```bash
python demo_basic.py
```

### Ví dụ 2: Sử dụng Proxy & Tự động khớp vị trí (`demo_proxy.py`)
Khi thêm proxy, bật `geoip=True` để trình duyệt tự động đồng bộ:
- Múi giờ (Timezone)
- Ngôn ngữ (Locale)
- Toạ độ GPS (Geolocation)
- Địa chỉ IP rò rỉ qua WebRTC
```bash
python demo_proxy.py
```

### Ví dụ 3: Lưu phiên đăng nhập & Tạo Profile riêng biệt (`demo_persistent_profile.py`)
Tương tự như Gologin hay AdsPower, `persistent_context=True` cùng với `user_data_dir` sẽ giúp lưu lại toàn bộ cookie, cache, lịch sử và trạng thái đăng nhập cho từng tài khoản riêng biệt:
```bash
python demo_persistent_profile.py
```

---

## 4. Các tùy chọn quan trọng của Camoufox
Khi khởi tạo `Camoufox(...)`, bạn có thể truyền các tham số:
- `headless`: `False` (hiện cửa sổ) hoặc `True` (chạy ngầm).
- `os`: `"windows"`, `"macos"`, hoặc `"linux"` (hệ điều hành muốn giả lập).
- `proxy`: Dictionary cấu hình proxy `{"server": "http://ip:port", "username": "...", "password": "..."}`.
- `geoip`: `True` (tự động lấy theo IP proxy) hoặc truyền chuỗi IP cụ thể.
- `humanize`: `True` (mô phỏng thao tác di chuột tự nhiên như con người).
- `screen`: Tùy chỉnh độ phân giải màn hình.
- `i_know_what_im_doing`: `True` (bỏ qua các thông báo cảnh báo về canvas noise khi giả lập OS khác).

