# Hướng Dẫn Sử Dụng Camoufox Antidetect Browser

## 1. Mở Ứng Dụng Desktop (Giao diện Quản lý Profile)
Bạn có thể mở ứng dụng theo 2 cách cực kỳ nhanh chóng:

* **Cách 1 (Khuyên dùng - Click đúp chuột):**
  - Mở thư mục này trong Finder và nhấp đúp chuột vào file:
    👉 **`Camoufox Antidetect.app`** hoặc file **`Chay_Ung_Dung.command`**
* **Cách 2 (Mở qua Terminal):**
  ```bash
  source .venv/bin/activate
  python app.py
  ```

---

## 2. Các Tính Năng Trên Giao Diện Desktop
1. **➕ Tạo Profile Mới**:
   - Nhập tên profile (ví dụ: *TikTok Shop 01*, *YouTube Channel A*).
   - Chọn hệ điều hành muốn giả lập: **Windows** (khuyên dùng để giống số đông), **macOS**, hoặc **Linux**.
   - Cấu hình Proxy: Hỗ trợ tất cả định dạng:
     - `ip:port` (Proxy không user/pass)
     - `ip:port:user:pass` (Định dạng proxy mua tại Việt Nam)
     - `http://user:pass@ip:port` hoặc `socks5://...`
   - URL mặc định khi mở: Đã gợi ý sẵn TikTok, YouTube, Browserleaks kiểm tra IP, Google,...
   - Ghi chú: Lưu thông tin tài khoản, mật khẩu, email để tiện theo dõi.
2. **🚀 Mở Trình Duyệt (Launch)**:
   - Nhấn nút **"Mở"** tại bất kỳ profile nào để khởi chạy Camoufox.
   - Trình duyệt sẽ mở ra với cấu hình phần cứng độc lập, cookie/session độc lập và IP theo proxy (nếu có).
   - Bạn có thể mở nhiều profile cùng một lúc.
3. **⏹ Dừng Trình Duyệt**:
   - Đóng cửa sổ trình duyệt hoặc nhấn nút **"Dừng"** trên app để tắt. Trạng thái sẽ tự động cập nhật về `⚪ Đã tắt`.
4. **✏️ Sửa / 🗑 Xóa Profile**:
   - Chỉnh sửa lại thông tin, proxy hoặc xóa bỏ profile cùng dữ liệu liên quan.
5. **📁 Mở Thư Mục Lưu Trữ**:
   - Nhấn nút **"📁 Mở thư mục"** ở thanh trên cùng để mở thư mục lưu dữ liệu cookie của tất cả profile.

---

## 3. Chạy Bằng Code Script (Tự Động Hóa / Bot)
Nếu bạn muốn viết code tự động cào dữ liệu hoặc tương tác TikTok/YouTube tự động:
- Xem code mẫu cơ bản: `demo_basic.py`
- Xem code mẫu kèm Proxy: `demo_proxy.py`
- Xem code mẫu lưu Profile: `demo_persistent_profile.py`
