import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# ===== API =====
API_URL = "http://147.135.212.197/crapi/st/viewstats"
TOKEN = "RFdUREJBUzR9T4dVc49ndmFra1NYV5CIhpGVcnaOYmqHhJZXfYGJSQ=="

params = {
    "token": TOKEN,
    "records": ""
}

# ===== TELEGRAM TOKEN =====
BOT_TOKEN = "8797797157:AAFAKZ9UsCvfxhyOMNDRTg4Nl6LhqpI7wyc"


# ===== GET NUMBER =====
def get_number():
    try:
        r = requests.get(API_URL, params=params)
        data = r.json()
        return data.get("number")
    except:
        return None


# ===== GET CODE =====
def get_code():
    try:
        r = requests.get(API_URL, params=params)
        data = r.json()
        return data.get("code")
    except:
        return None


# ===== START =====
def start(update, context):

    keyboard = [
        [InlineKeyboardButton("📱 Get Temp Number", callback_data="number")],
        [InlineKeyboardButton("🔄 Check Code", callback_data="code")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "✨ *Welcome to Temp Number Bot*\n\n"
        "📲 WhatsApp verification لپاره موقتي نمبر ترلاسه کړئ.\n\n"
        "👇 لاندې بټن وکاروئ."
    )

    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


# ===== BUTTON HANDLER =====
def button(update, context):

    query = update.callback_query
    query.answer()

    if query.data == "number":

        number = get_number()

        if number:
            text = f"📱 *Your Temporary Number*\n\n`{number}`\n\nWhatsApp کې یې استعمال کړه."
        else:
            text = "❌ Number ترلاسه نشو."

        keyboard = [
            [InlineKeyboardButton("🔄 Check Code", callback_data="code")]
        ]

        query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == "code":

        code = get_code()

        if code:
            text = f"✅ *WhatsApp Code*\n\n`{code}`"
        else:
            text = "⌛ لا تر اوسه کد نه دی راغلی."

        keyboard = [
            [InlineKeyboardButton("🔄 Refresh Code", callback_data="code")],
            [InlineKeyboardButton("📱 New Number", callback_data="number")]
        ]

        query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )


# ===== MAIN =====
def main():

    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("Bot Running...")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
