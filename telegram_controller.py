import os
import html
import threading
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from platform_utils import load_config
from post_manager import (
    get_video_record, update_video_status, add_tracked_channel,
    get_all_channels, force_publish_draft, delete_tiktok_video_and_file
)

_bot_instance: telebot.TeleBot | None = None
_bot_token_used: str = ""

def get_bot() -> telebot.TeleBot | None:
    global _bot_instance, _bot_token_used
    cfg = load_config()
    token = cfg.get("telegram_bot_token", "").strip() or os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return None
    if _bot_instance is None or _bot_token_used != token:
        _bot_instance = telebot.TeleBot(token, parse_mode="HTML")
        _bot_token_used = token
        _register_handlers(_bot_instance)
    return _bot_instance

def build_action_keyboard(video_id: str, action: str, yt_video_url: str = "") -> InlineKeyboardMarkup:
    """Tạo bàn phím Inline Keyboard ngay dưới tin nhắn báo cáo."""
    markup = InlineKeyboardMarkup(row_width=2)
    action_buttons = []
    if action == "DRAFTED":
        action_buttons.append(InlineKeyboardButton("🚀 Đăng TikTok nháp", callback_data=f"pub:{video_id}"))
        action_buttons.append(InlineKeyboardButton("🗑️ Xóa nháp TikTok", callback_data=f"del:{video_id}"))
    elif action == "PUBLISHED":
        action_buttons.append(InlineKeyboardButton("🗑️ Xóa video & File gốc", callback_data=f"del:{video_id}"))

    if yt_video_url:
        action_buttons.append(InlineKeyboardButton("📺 Xem Shorts trên YouTube", url=yt_video_url))

    if action_buttons:
        markup.add(*action_buttons)

    btn_add_ch = InlineKeyboardButton("➕ Thêm kênh nguồn", callback_data="cmd:add_guide")
    btn_list_ch = InlineKeyboardButton("📋 DS Kênh đang chạy", callback_data="cmd:list_channels")
    markup.add(btn_add_ch, btn_list_ch)
    return markup

def send_telegram_report_with_buttons(
    video_id: str,
    action: str,
    source_channel: str,
    tiktok_user: str,
    vpn_region: str,
    profile_name: str,
    shorts_title: str,
    quality_str: str,
    duration: float,
    check_status: str,
    caption_text: str,
    youtube_url: str,
    yt_status: str = "NONE",
    yt_video_url: str = ""
):
    """Gửi thông báo định dạng HTML chuẩn kèm bàn phím tương tác 2 chiều về Telegram."""
    bot = get_bot()
    if not bot:
        return

    cfg = load_config()
    chat_id = cfg.get("telegram_chat_id", "").strip() or os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not chat_id:
        return

    now_str = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    safe_channel = html.escape(source_channel)
    safe_user = html.escape(tiktok_user)
    safe_title = html.escape(shorts_title)
    safe_caption = html.escape(caption_text)

    if action == "PUBLISHED" or yt_status == "PUBLISHED":
        header = "🎉 <b>[AUTO ĐĂNG BÀI] HOÀN TẤT XỬ LÝ VIDEO!</b>"
    elif action == "DRAFTED":
        header = "⚠️ <b>[AUTO ĐĂNG BÀI] CẢNH BÁO TIKTOK - ĐÃ LƯU NHÁP!</b>"
    else:
        header = "ℹ️ <b>[AUTO ĐĂNG BÀI] BÁO CÁO TIẾN TRÌNH</b>"

    tt_line = ""
    if tiktok_user:
        shield = "🛡️ " if action == "PUBLISHED" else ("🚨 " if action == "DRAFTED" else "⏳ ")
        tt_line = f"🎵 <b>TikTok ({safe_user}):</b> {shield}{check_status}\n"

    yt_line = ""
    if yt_status != "NONE":
        yt_shield = "🎬 " if yt_status == "PUBLISHED" else "⚠️ "
        yt_line = f"📺 <b>YouTube Studio:</b> {yt_shield}{yt_status}\n"
        if yt_video_url:
            yt_line += f"   👉 <a href=\"{yt_video_url}\">Link Shorts đã đăng</a>\n"

    message_html = (
        f"{header}\n\n"
        f"👤 <b>Kênh nguồn:</b> {safe_channel}\n"
        f"🌐 <b>Vùng VPN:</b> {vpn_region} | <b>Profile:</b> {profile_name}\n"
        f"----------------------------------------\n"
        f"🎬 <b>Tiêu đề Shorts:</b> {safe_title}\n"
        f"📐 <b>Chất lượng thực tế:</b> {quality_str}\n"
        f"⏱️ <b>Thời lượng:</b> {duration}s (Chuẩn ≤ 59s)\n"
        f"----------------------------------------\n"
        f"{tt_line}"
        f"{yt_line}"
        f"⏰ <b>Thời gian đăng:</b> {now_str}\n\n"
        f"📝 <b>Caption đăng tải:</b>\n"
        f"<blockquote>{safe_caption}</blockquote>\n\n"
        f"🔗 <a href=\"{youtube_url}\">Xem video gốc nguồn</a>\n\n"
        f"🤖 <i>Hệ thống Auto Đăng Bài TikTok Beta & YouTube Shorts</i>"
    )
    keyboard = build_action_keyboard(video_id, action, yt_video_url)
    try:
        bot.send_message(
            chat_id=chat_id,
            text=message_html,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"[Telegram Send Error]: {e}")

def _register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_inline_buttons(call):
        data = call.data
        if data.startswith("pub:"):
            video_id = data.split(":", 1)[1]
            record = get_video_record(video_id)
            if not record:
                bot.answer_callback_query(call.id, "❌ Không tìm thấy dữ liệu video!", show_alert=True)
                return

            bot.answer_callback_query(call.id, f"⏳ Đang mở Camoufox Profile {record['profile_name']} để đăng nháp...")
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

            def _publish_task():
                ok = force_publish_draft(record)
                if ok:
                    bot.send_message(call.message.chat.id, f"✅ Đã đăng thành công bản nháp video <b>{record['shorts_title']}</b> lên TikTok!")
                else:
                    bot.send_message(call.message.chat.id, f"❌ Không thể đăng bản nháp. Vui lòng kiểm tra lại trình duyệt!")

            threading.Thread(target=_publish_task, daemon=True).start()

        elif data.startswith("del:"):
            video_id = data.split(":", 1)[1]
            record = get_video_record(video_id)
            if not record:
                bot.answer_callback_query(call.id, "❌ Không tìm thấy dữ liệu video!", show_alert=True)
                return

            bot.answer_callback_query(call.id, f"⏳ Đang xóa file & video trên TikTok...")
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

            def _delete_task():
                ok = delete_tiktok_video_and_file(record)
                if ok:
                    bot.send_message(call.message.chat.id, f"🗑️ Đã xóa video <b>{record['shorts_title']}</b> và file 4K thành công!")
                else:
                    bot.send_message(call.message.chat.id, f"⚠️ Đã xóa dữ liệu cục bộ nhưng có lỗi khi xóa trên TikTok Studio.")

            threading.Thread(target=_delete_task, daemon=True).start()

        elif data == "cmd:list_channels":
            channels = get_all_channels()
            if not channels:
                bot.answer_callback_query(call.id, "Danh sách trống!")
                bot.send_message(call.message.chat.id, "📋 Chưa có kênh nào được cấu hình theo dõi.")
                return

            lines = ["📋 <b>DANH SÁCH KÊNH ĐANG THEO DÕI:</b>\n"]
            for idx, ch in enumerate(channels, 1):
                lines.append(
                    f"{idx}. <b>{ch.get('profile_name', 'NoProfile')}</b> ({ch.get('vpn_region', 'VN')})\n"
                    f"   🔗 {ch.get('youtube_shorts_url')}\n"
                    f"   👤 TikTok: {ch.get('tiktok_user', 'N/A')} | Ngách: {ch.get('niche', 'N/A')}\n"
                )
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "\n".join(lines), disable_web_page_preview=True)

        elif data == "cmd:add_guide":
            bot.answer_callback_query(call.id)
            guide = (
                "➕ <b>HƯỚNG DẪN THÊM KÊNH TỰ ĐỘNG QUA TELEGRAM:</b>\n\n"
                "Hãy gửi tin nhắn theo đúng cú pháp sau:\n"
                "<code>/add [Link_YouTube_Shorts] | [TikTok_User] | [Vùng_VPN] | [Tên_Profile] | [Proxy_Server] | [Ngách]</code>\n\n"
                "<i>Ví dụ:</i>\n"
                "<code>/add https://youtube.com/@RedBull/shorts | @pilot_pov | US | US_01 | | Stunt Aviation POV</code>"
            )
            bot.send_message(call.message.chat.id, guide, disable_web_page_preview=True)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(
            message,
            "🤖 <b>Chào mừng bạn đến với Hệ thống Auto Đăng Bài Camoufox Antidetect!</b>\n\n"
            "Các lệnh hỗ trợ:\n"
            "• /channels - Xem danh sách các kênh đang theo dõi\n"
            "• /status - Xem trạng thái hệ thống\n"
            "• /add [thông tin kênh] - Thêm kênh quét tự động\n"
        )

    @bot.message_handler(commands=['channels'])
    def list_ch_cmd(message):
        channels = get_all_channels()
        if not channels:
            bot.reply_to(message, "📋 Chưa có kênh nào trong hệ thống.")
            return
        lines = ["📋 <b>DANH SÁCH KÊNH THEO DÕI:</b>\n"]
        for idx, ch in enumerate(channels, 1):
            lines.append(f"{idx}. <b>{ch.get('profile_name')}</b>: {ch.get('youtube_shorts_url')}")
        bot.reply_to(message, "\n".join(lines), disable_web_page_preview=True)

    @bot.message_handler(commands=['add'])
    def add_ch_cmd(message):
        text = message.text.replace("/add", "").strip()
        parts = [p.strip() for p in text.split("|")]
        if len(parts) < 4:
            bot.reply_to(message, "❌ Cú pháp chưa đúng! Gửi <code>/add [Link_YT] | [TikTok_User] | [VPN] | [Profile] | [Proxy] | [Niche]</code>")
            return
        yt_url = parts[0]
        tt_user = parts[1]
        vpn = parts[2]
        profile = parts[3]
        proxy = parts[4] if len(parts) > 4 else ""
        niche = parts[5] if len(parts) > 5 else ""
        try:
            add_tracked_channel(yt_url, tt_user, vpn, profile, "", proxy, niche)
            bot.reply_to(message, f"✅ Đã thêm kênh <b>{yt_url}</b> cho Profile <b>{profile}</b>!")
        except Exception as e:
            bot.reply_to(message, f"❌ Lỗi: {e}")

_tele_polling_thread = None

def start_telegram_polling_thread():
    global _tele_polling_thread
    bot = get_bot()
    if not bot:
        return None
    if _tele_polling_thread is not None and _tele_polling_thread.is_alive():
        return _tele_polling_thread

    def _poll():
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=15)
        except Exception as e:
            print(f"[Telegram Polling Stopped]: {e}")

    _tele_polling_thread = threading.Thread(target=_poll, daemon=True)
    _tele_polling_thread.start()
    return _tele_polling_thread

