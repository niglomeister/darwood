from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

from config import TOKEN 
from handlers import *

# Main bot entry point
def main():
    application = Application.builder().token(TOKEN).build()

    # Profile creation conversation handler
    profile_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(["👤 Мой профиль"]), create_profile)],
        states={
            PARENT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, parent_name)],
            CHILD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, child_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            GRADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, grade)],
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, goal)],
            TIMEZONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, timezone)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, contact)],
        },
        fallbacks=[CommandHandler("cancel", cancel_profile_creation)],
        per_user=True
    )

    # Add handlers
    application.add_handler(profile_conv_handler)
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()