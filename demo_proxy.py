from camoufox.sync_api import Camoufox

def main():
    # Cấu hình proxy nếu bạn có (HTTP hoặc SOCKS5)
    # geoip=True giúp tự động đồng bộ Timezone, Ngôn ngữ, Vị trí GPS và WebRTC theo IP của proxy!
    proxy_config = {
        "server": "http://username:password@ip:port",
    }
    
    # Nếu chưa có proxy, bạn có thể truyền IP cụ thể vào geoip="x.x.x.x" để test giả lập địa chỉ IP
    with Camoufox(
        headless=False,
        # proxy=proxy_config,
        # geoip=True,
        humanize=True, # Di chuyển chuột tự nhiên giống người thật
        i_know_what_im_doing=True
    ) as browser:
        page = browser.new_page()
        page.goto("https://browserleaks.com/ip")
        page.wait_for_timeout(5000)

if __name__ == "__main__":
    main()

