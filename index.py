import os
import logging
from flask import Flask, request, jsonify
import telebot
from telebot import types

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("dragon-x-vercel")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip()
OWNER_ID = int(os.getenv("OWNER_ID", "0") or "0")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "https://t.me/").strip()
UPDATE_GROUP = os.getenv("UPDATE_GROUP", "https://t.me/").strip()
CONTACT_USERNAME = os.getenv("CONTACT_USERNAME", "https://t.me/").strip()

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None


def main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("📢 Updates", url=UPDATE_CHANNEL),
        types.InlineKeyboardButton("👥 Group", url=UPDATE_GROUP),
        types.InlineKeyboardButton("👤 Profile", callback_data="profile"),
        types.InlineKeyboardButton("📤 Upload", callback_data="upload_info"),
        types.InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        types.InlineKeyboardButton("📞 Contact", url=CONTACT_USERNAME),
    )
    return kb


if bot:
    @bot.message_handler(commands=["start"])
    def start(message):
        name = message.from_user.first_name or "there"
        bot.send_message(
            message.chat.id,
            f"🐉 Welcome {name}!\n\nDRAGON X BOT is online.\nChoose an option:",
            reply_markup=main_menu(),
        )

    @bot.message_handler(commands=["help"])
    def help_command(message):
        bot.send_message(
            message.chat.id,
            "Available commands:\n/start — Open menu\n/help — Show help\n\n"
            "This Vercel edition handles Telegram messages using webhooks. "
            "It does not run uploaded Python/JavaScript files or provide a remote terminal."
        )

    @bot.callback_query_handler(func=lambda call: True)
    def callbacks(call):
        if call.data == "profile":
            user = call.from_user
            bot.answer_callback_query(call.id)
            bot.send_message(
                call.message.chat.id,
                f"👤 Profile\nName: {user.first_name or '-'}\n"
                f"User ID: {user.id}\nUsername: @{user.username}" if user.username
                else f"👤 Profile\nName: {user.first_name or '-'}\nUser ID: {user.id}"
            )
        elif call.data == "upload_info":
            bot.answer_callback_query(call.id)
            bot.send_message(
                call.message.chat.id,
                "📤 File upload/hosting is not enabled in this Vercel version. "
                "Vercel Functions are not designed to run user-uploaded scripts or keep them running."
            )
        elif call.data == "help":
            bot.answer_callback_query(call.id)
            bot.send_message(
                call.message.chat.id,
                "Use /start to open the menu. This version supports webhook-based bot replies."
            )
        else:
            bot.answer_callback_query(call.id, "Unknown option")


@app.get("/")
def home():
    return jsonify(
        status="ok",
        bot_configured=bool(bot),
        service="DRAGON X Telegram webhook"
    )


@app.post("/webhook")
def webhook():
    if not bot:
        return jsonify(error="BOT_TOKEN environment variable is missing"), 503

    if not WEBHOOK_SECRET:
        return jsonify(error="WEBHOOK_SECRET environment variable is missing"), 503

    supplied_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if supplied_secret != WEBHOOK_SECRET:
        return jsonify(error="unauthorized"), 401

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify(error="invalid JSON"), 400

    try:
        update = types.Update.de_json(payload)
        bot.process_new_updates([update])
    except Exception:
        log.exception("Failed to process Telegram update")
        return jsonify(error="update processing failed"), 500

    return jsonify(ok=True)


@app.get("/health")
def health():
    return jsonify(ok=True, bot_configured=bool(bot))
