from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
from database import save_user_profile, get_user_profile

import re 


def contains_numbers(s):
    return bool(re.search(r'\d', s))
def is_valid_phone(phone):
    pattern = r'^(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
    return bool(re.match(pattern, phone.strip()))



# Conversation states
PARENT_NAME, CHILD_NAME, AGE, GRADE, GOAL, TIMEZONE, CONTACT = range(7)


# Define the function to send the main menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_main_menu(update, context)

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if the user has already created a profile
    user_profile = get_user_profile(user_id)
    if not user_profile:
        # Menu before profile creation
        menu_keyboard = [
            [KeyboardButton("👤 Мой профиль")],
            [KeyboardButton("🎓 Вводный урок")]
        ]

        reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
        await update.message.reply_text("Главное меню:", reply_markup=reply_markup)
    else:
        # Menu after profile creation
        menu_keyboard = [
            [KeyboardButton("📚 Домашнее задание"), KeyboardButton("📝 Записаться на урок")],
            [KeyboardButton("❌ Отменить урок"), KeyboardButton("🔁 Перенести урок")],
            [KeyboardButton("🏅 Награды"), KeyboardButton("🛠️ Редактировать профиль")],
            [KeyboardButton("ℹ️ Информация"), KeyboardButton("🧑‍🏫 Связь с учителем")]
        ]


        reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
        await update.message.reply_text(f" Hello {user_profile['parent_name']}, Главное меню:", reply_markup=reply_markup)


# Profile creation handlers
async def create_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the profile creation process"""
    await update.message.reply_text(
        "🧾 Создание профиля ученика\n\n"
        "Пожалуйста, введите ФИО родителя:",
        reply_markup=ReplyKeyboardRemove()
    )
    return PARENT_NAME

async def parent_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle parent name input"""
    context.user_data['parent_name'] = update.message.text
    await update.message.reply_text(
        "👨‍👩‍👧‍👦 ФИО родителя: ✅\n\n"
        "Теперь введите ФИО ребёнка:"
    )
    return CHILD_NAME

async def child_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle child name input"""
    context.user_data['child_name'] = update.message.text
    await update.message.reply_text(
        "🧒 ФИО ребёнка: ✅\n\n"
        "Введите возраст ребёнка:"
    )
    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle age input"""
    try:
        age_value = int(update.message.text)
        if age_value < 1 or age_value > 18:
            await update.message.reply_text(
                "Пожалуйста, введите корректный возраст (от 1 до 18 лет):"
            )
            return AGE

        context.user_data['age'] = age_value
        await update.message.reply_text(
            "Введите класс ребёнка:"
        )
        return GRADE
    except ValueError:
        await update.message.reply_text(
            "Пожалуйста, введите возраст цифрами:"
        )
        return AGE

async def grade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle grade input"""
    try:
        context.user_data['grade'] = int(update.message.text)
        await update.message.reply_text(
            "Цель обучения:"
        )
        return GOAL
    except ValueError:
        await update.message.reply_text(
            "Пожалуйста, введите класс цифрами:"
        )
        return GRADE        

async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle learning goal input"""
    context.user_data['goal'] = update.message.text

    # Timezone keyboard
    timezone_keyboard = [
        [KeyboardButton("UTC+3"), KeyboardButton("UTC+4"), KeyboardButton("UTC+5")],
        [KeyboardButton("Другой часовой пояс")]
    ]
    reply_markup = ReplyKeyboardMarkup(timezone_keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🎯 Цель обучения: ✅\n\n"
        "Выберите ваш часовой пояс:",
        reply_markup=reply_markup
    )
    return TIMEZONE

async def timezone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle timezone input"""
    timezone_text = update.message.text

    if timezone_text == "Другой часовой пояс":
        await update.message.reply_text(
            "Введите ваш часовой пояс вручную (например, UTC+3):",
            reply_markup=ReplyKeyboardRemove()
        )
        return TIMEZONE

    context.user_data['timezone'] = timezone_text

    # Contact method keyboard
    contact_keyboard = [
        [KeyboardButton("Telegram")],
        [KeyboardButton("WhatsApp")]
    ]
    reply_markup = ReplyKeyboardMarkup(contact_keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🌍 Часовой пояс: ✅\n\n"
        "Выберите предпочитаемый способ связи:",
        reply_markup=reply_markup
    )
    return CONTACT

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle contact method selection"""
    contact_method = update.message.text

    if contact_method == "Telegram":
        username = update.effective_user.username
        if username:
            context.user_data['contact'] = f"Telegram: @{username}"
        else:
            context.user_data['contact'] = f"Telegram: {update.effective_user.first_name}"
    elif contact_method == "WhatsApp":
        await update.message.reply_text(
            "Введите ваш номер WhatsApp:",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data['contact_method'] = 'whatsapp'
        return CONTACT
    else:
        # This handles manual timezone input or WhatsApp number
        if 'contact_method' in context.user_data and context.user_data['contact_method'] == 'whatsapp':
            context.user_data['contact'] = f"WhatsApp: {update.message.text}"
        else:
            # Manual timezone input
            context.user_data['timezone'] = update.message.text
            contact_keyboard = [
                [KeyboardButton("Telegram")],
                [KeyboardButton("WhatsApp")]
            ]
            reply_markup = ReplyKeyboardMarkup(contact_keyboard, resize_keyboard=True)

            await update.message.reply_text(
                "🌍 Часовой пояс: ✅\n\n"
                "Выберите предпочитаемый способ связи:",
                reply_markup=reply_markup
            )
            return CONTACT

    # Save the profile
    user_id = update.effective_user.id
    profile_data = {
        'parent_name': context.user_data['parent_name'],
        'child_name': context.user_data['child_name'],
        'age': context.user_data['age'],
        'grade': context.user_data['grade'],
        'goal': context.user_data['goal'],
        'timezone': context.user_data['timezone'],
        'contact': context.user_data['contact']
    }

    save_user_profile(user_id, profile_data)

    # Show summary
    summary = (
        "✅ Профиль успешно создан!\n\n"
        f"👨‍👩‍👧‍👦 ФИО родителя: {profile_data['parent_name']}\n"
        f"🧒 ФИО ребёнка: {profile_data['child_name']}\n"
        f"🎂 Возраст: {profile_data['age']}\n"
        f"🏫 Класс: {profile_data['grade']}\n"
        f"🎯 Цель обучения: {profile_data['goal']}\n"
        f"🌍 Часовой пояс: {profile_data['timezone']}\n"
        f"📱 Контакт: {profile_data['contact']}"
    )

    await update.message.reply_text(summary, reply_markup=ReplyKeyboardRemove())

    # Clear user data
    context.user_data.clear()

    # Return to main menu
    await send_main_menu(update, context)
    return ConversationHandler.END

async def cancel_profile_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel profile creation"""
    context.user_data.clear()
    await update.message.reply_text(
        "Создание профиля отменено.",
        reply_markup=ReplyKeyboardRemove()
    )
    await send_main_menu(update, context)
    return ConversationHandler.END
   
def profile_conv_handler():
    return ConversationHandler(
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