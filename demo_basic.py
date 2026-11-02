from camoufox.sync_api import Camoufox

def main():
    # Khởi chạy Camoufox (có giao diện: headless=False, chạy ngầm: headless=True)
    # i_know_what_im_doing=True để tắt cảnh báo LeakWarning khi giả lập OS khác
    with Camoufox(headless=False, i_know_what_im_doing=True) as browser:
        page = browser.new_page()
        
        print("Đang mở trang kiểm tra fingerprint...")
        page.goto("https://browserleaks.com/javascript")
        
        # In tiêu đề trang
        print("Tiêu đề trang:", page.title())
        
        # Đợi 5 giây để quan sát giao diện
        page.wait_for_timeout(5000)

if __name__ == "__main__":
    main()

