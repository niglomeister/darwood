from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler



# Conversation states
PARENT_NAME, CHILD_NAME, AGE, GRADE, GOAL, TIMEZONE, CONTACT = range(7)

#placeholder for now, will check the database later
def get_user(user_id : int):
    return None

def save_user_profile(user_id: int, profile_data: dict):
    """Placeholder function to save user profile to database"""
    print(f"Saving profile for user {user_id}: {profile_data}")
    # Here you would save to your database
    pass



# Define the function to send the main menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_main_menu(update, context)

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
   