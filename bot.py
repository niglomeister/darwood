from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from config import TOKEN 

#placeholder for now, will check the database later
def get_user(user_id : int):
    return None


# Define the start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if the user exists (always returns None in this placeholder)
    user = get_user(user_id)

    if user is None:
        # Greet and offer the "🚀 Start" button
        start_keyboard = [[KeyboardButton("🚀 Старт")]]
        reply_markup = ReplyKeyboardMarkup(start_keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Привет! Добро пожаловать в Бота! Нажмите «🚀 Старт» для продолжения.",
            reply_markup=reply_markup
        )
    else:
        # The profile already exists, send the main menu
        await send_main_menu(update, context)


# Define the handler for the "🚀 Старт" button
async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_main_menu(update, context)


# Define the function to send the main menu
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if the user has already created a profile
    if get_user(user_id) is None:
        # Menu before profile creation
        menu_keyboard = [
            [KeyboardButton("👤 Мой профиль")],
            [KeyboardButton("🎓 Вводный урок")]
        ]
    else:
        # Menu after profile creation
        menu_keyboard = [
            [KeyboardButton("📚 Домашнее задание"), KeyboardButton("📝 Записаться на урок")],
            [KeyboardButton("❌ Отменить урок"), KeyboardButton("🔁 Перенести урок")],
            [KeyboardButton("🏅 Награды"), KeyboardButton("🛠️ Редактировать профиль")],
            [KeyboardButton("ℹ️ Информация"), KeyboardButton("🧑‍🏫 Связь с учителем")]
        ]

    reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
    await update.message.reply_text("Главное меню:", reply_markup=reply_markup)


# Main bot entry point
def main():
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Message handler for "🚀 Старт"
    application.add_handler(MessageHandler(filters.Text(["🚀 Старт"]), handle_start_button))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()