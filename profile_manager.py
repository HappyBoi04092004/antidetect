import os
import json
import uuid
import time
import shutil

PROFILES_FILE = "profiles.json"
PROFILES_DIR = "profiles"

def sync_autologin_file(profile_data):
    try:
        p_path = profile_data.get("path")
        if not p_path or not os.path.exists(p_path):
            return
        auto_login = profile_data.get("auto_login", False)
        auto_login_type = profile_data.get("auto_login_type", "tiktok")
        account_str = profile_data.get("account_str", "") or profile_data.get("notes", "")
        
        from auto_login import parse_account_string
        creds = parse_account_string(account_str)
        
        cfg_path = os.path.join(p_path, "autologin.json")
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump({
                "enabled": bool(auto_login),
                "type": auto_login_type,
                "account_str": account_str,
                "creds": creds
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi khi đồng bộ autologin.json: {e}")

class ProfileManager:
    def __init__(self, profiles_file=PROFILES_FILE, profiles_dir=PROFILES_DIR):
        self.profiles_file = profiles_file
        self.profiles_dir = profiles_dir
        os.makedirs(self.profiles_dir, exist_ok=True)
        self.profiles = self.load_profiles()

    def load_profiles(self):
        if not os.path.exists(self.profiles_file):
            return []
        try:
            with open(self.profiles_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Tự động đồng bộ và nâng cấp trường auto-login cho profile cũ
                for p in data:
                    if "group" not in p or not p.get("group"):
                        p["group"] = "Mặc định"
                    if "auto_login" not in p:
                        p["auto_login"] = False
                    if "auto_login_type" not in p:
                        p["auto_login_type"] = "tiktok"
                    if "account_str" not in p:
                        p["account_str"] = p.get("notes", "") if "|" in p.get("notes", "") else ""
                    sync_autologin_file(p)
                return data
        except Exception:
            return []

    def save_profiles(self):
        with open(self.profiles_file, "w", encoding="utf-8") as f:
            json.dump(self.profiles, f, ensure_ascii=False, indent=2)

    def create_profile(
        self,
        name,
        group="Mặc định",
        os_type="windows",
        proxy="",
        start_url="https://browserleaks.com/ip",
        screen="1920x1080",
        locale="",
        block_images=False,
        block_webrtc=False,
        humanize=True,
        headless=False,
        disable_coop=False,
        canvas_noise=False,
        disable_ublock=False,
        addons="",
        notes="",
        auto_login=False,
        auto_login_type="tiktok",
        account_str=""
    ):
        profile_id = str(uuid.uuid4())[:8]
        profile_dir_path = os.path.join(self.profiles_dir, profile_id)
        os.makedirs(profile_dir_path, exist_ok=True)

        profile_data = {
            "id": profile_id,
            "name": name.strip() or f"Profile {profile_id}",
            "group": group.strip() or "Mặc định",
            "os": os_type,
            "proxy": proxy.strip(),
            "start_url": start_url.strip() or "https://browserleaks.com/ip",
            "screen": screen.strip() or "1920x1080",
            "locale": locale.strip(),
            "block_images": bool(block_images),
            "block_webrtc": bool(block_webrtc),
            "humanize": bool(humanize),
            "headless": bool(headless),
            "disable_coop": bool(disable_coop),
            "canvas_noise": bool(canvas_noise),
            "disable_ublock": bool(disable_ublock),
            "addons": addons.strip(),
            "notes": notes.strip(),
            "auto_login": bool(auto_login),
            "auto_login_type": auto_login_type.strip() if auto_login_type else "tiktok",
            "account_str": account_str.strip() or (notes.strip() if "|" in notes else ""),
            "path": profile_dir_path,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.profiles.append(profile_data)
        self.save_profiles()
        sync_autologin_file(profile_data)
        return profile_data

    def clone_profile(self, profile_id):
        orig = self.get_profile(profile_id)
        if not orig:
            return None

        new_id = str(uuid.uuid4())[:8]
        new_dir = os.path.join(self.profiles_dir, new_id)
        
        # Sao chép thư mục dữ liệu cookie nếu có
        if os.path.exists(orig["path"]):
            try:
                shutil.copytree(orig["path"], new_dir)
            except Exception:
                os.makedirs(new_dir, exist_ok=True)
        else:
            os.makedirs(new_dir, exist_ok=True)

        cloned = dict(orig)
        cloned["id"] = new_id
        cloned["name"] = f"{orig.get('name', 'Profile')} (Bản sao)"
        cloned["path"] = new_dir
        cloned["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        self.profiles.append(cloned)
        self.save_profiles()
        return cloned

    def update_profile(self, profile_id, **kwargs):
        for p in self.profiles:
            if p["id"] == profile_id:
                for k, v in kwargs.items():
                    p[k] = v
                self.save_profiles()
                sync_autologin_file(p)
                return p
        return None

    def delete_profile(self, profile_id, delete_data=True):
        for i, p in enumerate(self.profiles):
            if p["id"] == profile_id:
                if delete_data and os.path.exists(p["path"]):
                    try:
                        shutil.rmtree(p["path"])
                    except Exception as e:
                        print(f"Lỗi khi xóa thư mục {p['path']}: {e}")
                del self.profiles[i]
                self.save_profiles()
                return True
        return False

    def get_profile(self, profile_id):
        for p in self.profiles:
            if p["id"] == profile_id:
                return p
        return None
