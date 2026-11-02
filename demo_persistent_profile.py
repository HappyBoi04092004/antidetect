from camoufox.sync_api import Camoufox

def main():
    # persistent_context=True giúp lưu lại cookie, session, lịch sử đăng nhập vào thư mục chỉ định
    # Giống như bạn tạo 1 profile trên Gologin / AdsPower / MoreLogin
    user_data_path = "./profiles/profile_1"
    
    with Camoufox(
        headless=False,
        persistent_context=True,
        user_data_dir=user_data_path,
        humanize=True,
        i_know_what_im_doing=True
    ) as context:
        page = context.new_page()
        page.goto("https://google.com")
        print("Profile đã khởi chạy và dữ liệu lưu tại:", user_data_path)
        page.wait_for_timeout(5000)

if __name__ == "__main__":
    main()

