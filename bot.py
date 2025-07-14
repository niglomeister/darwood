from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
from telegram.ext import Application
from handlers.intro_lesson import get_intro_lesson_handler


from config import TOKEN 
from handlers.profile import *

# Main bot entry point


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(get_intro_lesson_handler())
    application.add_handler(profile_conv_handler())
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()