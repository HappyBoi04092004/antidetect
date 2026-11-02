import sys
import os
import argparse
import time
import threading
from urllib.parse import urlparse
from camoufox.sync_api import Camoufox
from camoufox.fingerprints import Screen
from camoufox.addons import DefaultAddons

def parse_proxy(proxy_str: str):
    if not proxy_str or not proxy_str.strip():
        return None
    s = proxy_str.strip()
    parts = s.split(":")
    if len(parts) == 4 and not ("://" in s):
        ip, port, user, pwd = parts
        return {"server": f"http://{ip}:{port}", "username": user, "password": pwd}
    if not ("://" in s):
        s = "http://" + s
    parsed = urlparse(s)
    res = {"server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"}
    if parsed.username:
        res["username"] = parsed.username
    if parsed.password:
        res["password"] = parsed.password
    return res

def main():
    parser = argparse.ArgumentParser(description="Camoufox Standalone Profile Runner")
    parser.add_argument("--profile-dir", required=True, help="Thư mục lưu profile")
    parser.add_argument("--os", default="windows", choices=["windows", "macos", "linux"], help="Hệ điều hành giả lập")
    parser.add_argument("--proxy", default="", help="Chuỗi proxy")
    parser.add_argument("--url", default="https://browserleaks.com/ip", help="Trang web mở ban đầu")
    parser.add_argument("--screen", default="1920x1080", help="Độ phân giải màn hình")
    parser.add_argument("--locale", default="", help="Ngôn ngữ trình duyệt")
    parser.add_argument("--block-images", action="store_true", help="Chặn tải hình ảnh")
    parser.add_argument("--block-webrtc", action="store_true", help="Vô hiệu hóa WebRTC")
    parser.add_argument("--disable-humanize", action="store_true", help="Tắt giả lập rê chuột")
    parser.add_argument("--headless", action="store_true", help="Chạy ở chế độ ẩn ngầm")
    parser.add_argument("--disable-coop", action="store_true", help="Tắt COOP để tự động click Turnstile iframe")
    parser.add_argument("--canvas-noise", action="store_true", help="Bật chống vân tay Canvas")
    parser.add_argument("--disable-ublock", action="store_true", help="Tắt tiện ích uBlock Origin")
    parser.add_argument("--addons", default="", help="Đường dẫn thư mục tiện ích mở rộng Firefox")
    parser.add_argument("--auto-login", action="store_true", help="Kích hoạt tự động đăng nhập")
    parser.add_argument("--auto-login-type", default="tiktok", help="Loại nền tảng tự động đăng nhập (tiktok)")

    args = parser.parse_args()

    profile_dir = os.path.abspath(args.profile_dir)
    os.makedirs(profile_dir, exist_ok=True)

    # Tự động dọn dẹp file khóa cũ (.parentlock) nếu phiên trước bị tắt đột ngột
    for lock_name in [".parentlock", "lock", "parent.lock"]:
        lp = os.path.join(profile_dir, lock_name)
        if os.path.exists(lp):
            try:
                os.remove(lp)
            except Exception:
                pass

    proxy_cfg = parse_proxy(args.proxy) if args.proxy else None
    has_proxy = proxy_cfg is not None

    print(f"[*] Khởi chạy Camoufox Profile: {profile_dir}")
    print(f"[*] OS Giả lập: {args.os}")
    print(f"[*] Proxy: {proxy_cfg['server'] if proxy_cfg else 'None (Mạng trực tiếp)'}")
    print(f"[*] Màn hình: {args.screen}")
    print(f"[*] URL ban đầu: {args.url}")

    camoufox_kwargs = {
        "headless": args.headless,
        "os": args.os,
        "persistent_context": True,
        "user_data_dir": profile_dir,
        "humanize": not args.disable_humanize,
        "block_images": args.block_images,
        "block_webrtc": args.block_webrtc,
        "disable_coop": args.disable_coop,
        "canvas_noise": args.canvas_noise,
        "i_know_what_im_doing": True,
    }

    # Quản lý tiện ích mở rộng (uBlock Origin mặc định)
    if args.disable_ublock:
        camoufox_kwargs["exclude_addons"] = [DefaultAddons.UBO]

    if args.addons.strip() and os.path.isdir(args.addons.strip()):
        camoufox_kwargs["addons"] = [args.addons.strip()]

    # Cấu hình kích thước màn hình
    if args.screen and "x" in args.screen:
        try:
            w, h = map(int, args.screen.lower().split("x"))
            camoufox_kwargs["screen"] = Screen(max_width=w, max_height=h)
        except Exception:
            pass

    # Cấu hình ngôn ngữ
    if args.locale.strip():
        camoufox_kwargs["locale"] = args.locale.strip()

    # Cấu hình Proxy & GeoIP
    if has_proxy:
        camoufox_kwargs["proxy"] = proxy_cfg
        camoufox_kwargs["geoip"] = True

    # Đọc cấu hình Auto-Login nếu có trong profile
    autologin_file = os.path.join(profile_dir, "autologin.json")
    autologin_cfg = None
    if os.path.exists(autologin_file):
        try:
            import json
            with open(autologin_file, "r", encoding="utf-8") as f:
                autologin_cfg = json.load(f)
        except Exception:
            pass

    should_auto_login = args.auto_login or (autologin_cfg and autologin_cfg.get("enabled"))
    app_type = (autologin_cfg.get("type") if autologin_cfg else None) or args.auto_login_type or "tiktok"

    try:
        with Camoufox(**camoufox_kwargs) as context:
            page = context.pages[0] if context.pages else context.new_page()
            
            if should_auto_login and autologin_cfg and autologin_cfg.get("creds"):
                print(f"[*] Kích hoạt tự động đăng nhập {app_type.upper()}...")
                try:
                    from auto_login import auto_login_tiktok
                    if app_type.lower() == "tiktok":
                        auto_login_tiktok(page, autologin_cfg["creds"], logger=print)
                except Exception as e:
                    print(f"[!] Lỗi khi tự động đăng nhập: {e}")
            elif args.url.strip():
                try:
                    page.goto(args.url.strip(), timeout=60000)
                except Exception as e:
                    print(f"[!] Không thể tải ngay URL ({args.url}): {e}")

            print("[*] Trình duyệt đang hoạt động. Giữ cửa sổ mở không giới hạn thời gian...")

            browser_closed = threading.Event()

            def on_close(_=None):
                browser_closed.set()

            context.on("close", on_close)

            while not browser_closed.is_set():
                try:
                    if len(context.pages) == 0:
                        time.sleep(1)
                        if len(context.pages) == 0:
                            print("[*] Người dùng đã đóng tất cả các tab. Thoát.")
                            break
                    time.sleep(1)
                except Exception:
                    break

    except Exception as e:
        print(f"[!] Lỗi khi chạy Camoufox: {e}", file=sys.stderr)
        sys.exit(1)

    print("[*] Profile đã đóng hoàn tất.")

if __name__ == "__main__":
    main()
