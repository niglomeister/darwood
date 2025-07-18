from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler, CallbackQueryHandler
from database import save_user_profile, get_user_profile
from utils import contains_numbers, is_valid_phone

import re

# Conversation states for editing
EDIT_FIELD_SELECT, EDIT_PARENT_NAME, EDIT_CHILD_NAME, EDIT_AGE, EDIT_GRADE, EDIT_GOAL, EDIT_TIMEZONE, EDIT_CONTACT = range(8)

async def edit_profile_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the profile editing process"""
    user_id = update.effective_user.id
    user_profile = get_user_profile(user_id)

    if not user_profile:
        await update.message.reply_text(
            "❌ У вас нет профиля для редактирования. Сначала создайте профиль.",
            reply_markup=ReplyKeyboardRemove()
        )
        # Import and call main menu function here
        from handlers.profile_handler import send_main_menu
        await send_main_menu(update, context)
        return ConversationHandler.END

    # Store current profile data
    context.user_data['current_profile'] = user_profile

    # Create inline keyboard for field selection
    keyboard = [
        [InlineKeyboardButton("👨‍👩‍👧‍👦 ФИО родителя", callback_data="edit_parent_name")],
        [InlineKeyboardButton("🧒 ФИО ребёнка", callback_data="edit_child_name")],
        [InlineKeyboardButton("🎂 Возраст", callback_data="edit_age")],
        [InlineKeyboardButton("🏫 Класс", callback_data="edit_grade")],
        [InlineKeyboardButton("🎯 Цель обучения", callback_data="edit_goal")],
        [InlineKeyboardButton("🌍 Часовой пояс", callback_data="edit_timezone")],
        [InlineKeyboardButton("📱 Контакт", callback_data="edit_contact")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")],
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel_edit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Show current profile and options
    profile_text = (
        "🛠️ **Редактирование профиля**\n\n"
        "**Текущие данные:**\n"
        f"👨‍👩‍👧‍👦 ФИО родителя: {user_profile['parent_name']}\n"
        f"🧒 ФИО ребёнка: {user_profile['child_name']}\n"
        f"🎂 Возраст: {user_profile['age']}\n"
        f"🏫 Класс: {user_profile['grade']}\n"
        f"🎯 Цель обучения: {user_profile['goal']}\n"
        f"🌍 Часовой пояс: {user_profile['timezone']}\n"
        f"📱 Контакт: {user_profile['contact']}\n\n"
        "Выберите поле для редактирования:"
    )

    # Hide main menu keyboard and show edit options
    await update.message.reply_text(
        profile_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    # Remove the main menu keyboard
    await update.message.reply_text(
        "🔧 Режим редактирования активирован...",
        reply_markup=ReplyKeyboardRemove()
    )

    return EDIT_FIELD_SELECT

async def handle_field_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle field selection for editing"""
    query = update.callback_query
    await query.answer()

    field = query.data
    current_profile = context.user_data['current_profile']

    if field == "cancel_edit" or field == "back_to_main":
        await query.edit_message_text("🏠 Возвращаемся в главное меню...")
        from handlers.profile_handler import send_main_menu
        await send_main_menu(update, context)
        context.user_data.clear()
        return ConversationHandler.END

    # Create a "Back" and "Cancel" keyboard for text input fields
    back_keyboard = [
        [KeyboardButton("🔙 Назад к выбору поля")],
        [KeyboardButton("🏠 Главное меню")],
        [KeyboardButton("❌ Отмена")]
    ]
    back_reply_markup = ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True)

    if field == "edit_parent_name":
        await query.edit_message_text(
            f"👨‍👩‍👧‍👦 **Изменение ФИО родителя**\n\n"
            f"Текущее значение: {current_profile['parent_name']}\n\n"
            f"Введите новое ФИО родителя (только буквы):",
            parse_mode='Markdown'
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите новое значение или выберите действие:",
            reply_markup=back_reply_markup
        )
        return EDIT_PARENT_NAME

    elif field == "edit_child_name":
        await query.edit_message_text(
            f"🧒 **Изменение ФИО ребёнка**\n\n"
            f"Текущее значение: {current_profile['child_name']}\n\n"
            f"Введите новое ФИО ребёнка (только буквы):",
            parse_mode='Markdown'
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите новое значение или выберите действие:",
            reply_markup=back_reply_markup
        )
        return EDIT_CHILD_NAME

    elif field == "edit_age":
        await query.edit_message_text(
            f"🎂 **Изменение возраста**\n\n"
            f"Текущее значение: {current_profile['age']}\n\n"
            f"Введите новый возраст (от 1 до 18):",
            parse_mode='Markdown'
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите новое значение или выберите действие:",
            reply_markup=back_reply_markup
        )
        return EDIT_AGE

    elif field == "edit_grade":
        await query.edit_message_text(
            f"🏫 **Изменение класса**\n\n"
            f"Текущее значение: {current_profile['grade']}\n\n"
            f"Введите новый класс (число от 1 до 11):",
            parse_mode='Markdown'
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите новое значение или выберите действие:",
            reply_markup=back_reply_markup
        )
        return EDIT_GRADE

    elif field == "edit_goal":
        await query.edit_message_text(
            f"🎯 **Изменение цели обучения**\n\n"
            f"Текущее значение: {current_profile['goal']}\n\n"
            f"Введите новую цель обучения:",
            parse_mode='Markdown'
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите новое значение или выберите действие:",
            reply_markup=back_reply_markup
        )
        return EDIT_GOAL

    elif field == "edit_timezone":
        timezone_keyboard = [
            [KeyboardButton("UTC+3"), KeyboardButton("UTC+4"), KeyboardButton("UTC+5")],
            [KeyboardButton("Другой часовой пояс")],
            [KeyboardButton("🔙 Назад к выбору поля")],
            [KeyboardButton("🏠 Главное меню"), KeyboardButton("❌ Отмена")]
        ]
        reply_markup = ReplyKeyboardMarkup(timezone_keyboard, resize_keyboard=True)

        await query.edit_message_text(
            f"🌍 **Изменение часового пояса**\n\n"
            f"Текущее значение: {current_profile['timezone']}",
            parse_mode='Markdown'
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите новый часовой пояс:",
            reply_markup=reply_markup
        )
        return EDIT_TIMEZONE

    elif field == "edit_contact":
        contact_keyboard = [
            [KeyboardButton("Telegram")],
            [KeyboardButton("WhatsApp")],
            [KeyboardButton("🔙 Назад к выбору поля")],
            [KeyboardButton("🏠 Главное меню"), KeyboardButton("❌ Отмена")]
        ]
        reply_markup = ReplyKeyboardMarkup(contact_keyboard, resize_keyboard=True)

        await query.edit_message_text(
            f"📱 **Изменение контакта**\n\n"
            f"Текущее значение: {current_profile['contact']}",
            parse_mode='Markdown'
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите новый способ связи:",
            reply_markup=reply_markup
        )
        return EDIT_CONTACT

# Individual field edit handlers
async def edit_parent_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle parent name editing"""
    if await handle_navigation_buttons(update, context):
        return ConversationHandler.END

    new_value = update.message.text.strip()

    # Validation: check if name contains numbers
    if contains_numbers(new_value):
        await update.message.reply_text(
            "❌ ФИО родителя не должно содержать цифры. Пожалуйста, введите только буквы:"
        )
        return EDIT_PARENT_NAME

    # Check if name is not empty and has reasonable length
    if len(new_value) < 2:
        await update.message.reply_text(
            "❌ ФИО родителя слишком короткое. Пожалуйста, введите полное ФИО:"
        )
        return EDIT_PARENT_NAME

    await save_field_and_finish(update, context, 'parent_name', new_value, "👨‍👩‍👧‍👦 ФИО родителя")
    return ConversationHandler.END

async def edit_child_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle child name editing"""
    if await handle_navigation_buttons(update, context):
        return ConversationHandler.END

    new_value = update.message.text.strip()

    # Validation: check if name contains numbers
    if contains_numbers(new_value):
        await update.message.reply_text(
            "❌ ФИО ребёнка не должно содержать цифры. Пожалуйста, введите только буквы:"
        )
        return EDIT_CHILD_NAME

    # Check if name is not empty and has reasonable length
    if len(new_value) < 2:
        await update.message.reply_text(
            "❌ ФИО ребёнка слишком короткое. Пожалуйста, введите полное ФИО:"
        )
        return EDIT_CHILD_NAME

    await save_field_and_finish(update, context, 'child_name', new_value, "🧒 ФИО ребёнка")
    return ConversationHandler.END

async def edit_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle age editing"""
    if await handle_navigation_buttons(update, context):
        return ConversationHandler.END

    try:
        age_value = int(update.message.text.strip())
        if age_value < 1 or age_value > 18:
            await update.message.reply_text(
                "❌ Пожалуйста, введите корректный возраст (от 1 до 18 лет):"
            )
            return EDIT_AGE

        await save_field_and_finish(update, context, 'age', age_value, "🎂 Возраст")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введите возраст цифрами:"
        )
        return EDIT_AGE

async def edit_grade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle grade editing"""
    if await handle_navigation_buttons(update, context):
        return ConversationHandler.END

    try:
        grade_value = int(update.message.text.strip())
        if grade_value < 1 or grade_value > 11:
            await update.message.reply_text(
                "❌ Пожалуйста, введите корректный класс (от 1 до 11):"
            )
            return EDIT_GRADE

        await save_field_and_finish(update, context, 'grade', grade_value, "🏫 Класс")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введите класс цифрами:"
        )
        return EDIT_GRADE

async def edit_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle goal editing"""
    if await handle_navigation_buttons(update, context):
        return ConversationHandler.END

    new_value = update.message.text.strip()

    # Basic validation for goal
    if len(new_value) < 5:
        await update.message.reply_text(
            "❌ Цель обучения слишком короткая. Пожалуйста, опишите цель более подробно:"
        )
        return EDIT_GOAL

    await save_field_and_finish(update, context, 'goal', new_value, "🎯 Цель обучения")
    return ConversationHandler.END

async def edit_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle timezone editing"""
    timezone_text = update.message.text.strip()

    if await handle_navigation_buttons(update, context):
        return ConversationHandler.END

    if timezone_text == "Другой часовой пояс":
        back_keyboard = [
            [KeyboardButton("🔙 Назад к выбору поля")],
            [KeyboardButton("🏠 Главное меню")],
            [KeyboardButton("❌ Отмена")]
        ]
        await update.message.reply_text(
            "Введите ваш часовой пояс вручную (например, UTC+3, UTC-5, GMT+2):",
            reply_markup=ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True)
        )
        return EDIT_TIMEZONE

    # Basic validation for custom timezone format
    if not timezone_text.startswith(('UTC', 'GMT')) and timezone_text not in ['UTC+3', 'UTC+4', 'UTC+5']:
        # Check if it's a manual timezone input
        if 'UTC' in timezone_text or 'GMT' in timezone_text:
            # Allow it if it contains UTC or GMT
            pass
        else:
            await update.message.reply_text(
                "❌ Неверный формат часового пояса. Используйте формат UTC+3, GMT+2 и т.д.:"
            )
            return EDIT_TIMEZONE

    await save_field_and_finish(update, context, 'timezone', timezone_text, "🌍 Часовой пояс")
    return ConversationHandler.END

async def edit_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle contact editing"""
    contact_method = update.message.text.strip()

    if await handle_navigation_buttons(update, context):
        return ConversationHandler.END

    if contact_method == "Telegram":
        username = update.effective_user.username
        if username:
            new_contact = f"Telegram: @{username}"
        else:
            new_contact = f"Telegram: {update.effective_user.first_name}"
        await save_field_and_finish(update, context, 'contact', new_contact, "📱 Контакт")
        return ConversationHandler.END

    elif contact_method == "WhatsApp":
        back_keyboard = [
            [KeyboardButton("🔙 Назад к выбору поля")],
            [KeyboardButton("🏠 Главное меню")],
            [KeyboardButton("❌ Отмена")]
        ]
        await update.message.reply_text(
            "Введите ваш номер WhatsApp (в международном формате, например +7xxxxxxxxxx):",
            reply_markup=ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True)
        )
        context.user_data['editing_whatsapp'] = True
        return EDIT_CONTACT

    else:
        # Handle WhatsApp number input
        if context.user_data.get('editing_whatsapp'):
            phone_number = contact_method.strip()

            # Validate phone number
            if not is_valid_phone(phone_number):
                await update.message.reply_text(
                    "❌ Неверный формат номера телефона. Пожалуйста, введите номер в международном формате (+7xxxxxxxxxx):"
                )
                return EDIT_CONTACT

            new_contact = f"WhatsApp: {phone_number}"
            context.user_data.pop('editing_whatsapp', None)
            await save_field_and_finish(update, context, 'contact', new_contact, "📱 Контакт")
            return ConversationHandler.END
        else:
            # Invalid input
            await update.message.reply_text(
                "❌ Пожалуйста, выберите Telegram или WhatsApp, либо используйте кнопки навигации."
            )
            return EDIT_CONTACT

async def handle_navigation_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle navigation buttons (Back, Main Menu, Cancel)"""
    text = update.message.text

    if text == "🔙 Назад к выбору поля":
        await back_to_field_selection(update, context)
        return True
    elif text == "🏠 Главное меню":
        await go_to_main_menu(update, context)
        return True
    elif text == "❌ Отмена":
        await cancel_edit(update, context)
        return True

    return False

async def back_to_field_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to field selection"""
    current_profile = context.user_data.get('current_profile')
    if not current_profile:
        await go_to_main_menu(update, context)
        return

    # Create inline keyboard for field selection
    keyboard = [
        [InlineKeyboardButton("👨‍👩‍👧‍👦 ФИО родителя", callback_data="edit_parent_name")],
        [InlineKeyboardButton("🧒 ФИО ребёнка", callback_data="edit_child_name")],
        [InlineKeyboardButton("🎂 Возраст", callback_data="edit_age")],
        [InlineKeyboardButton("🏫 Класс", callback_data="edit_grade")],
        [InlineKeyboardButton("🎯 Цель обучения", callback_data="edit_goal")],
        [InlineKeyboardButton("🌍 Часовой пояс", callback_data="edit_timezone")],
        [InlineKeyboardButton("📱 Контакт", callback_data="edit_contact")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")],
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel_edit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    profile_text = (
        "🛠️ **Редактирование профиля**\n\n"
        "**Текущие данные:**\n"
        f"👨‍👩‍👧‍👦 ФИО родителя: {current_profile['parent_name']}\n"
        f"🧒 ФИО ребёнка: {current_profile['child_name']}\n"
        f"🎂 Возраст: {current_profile['age']}\n"
        f"🏫 Класс: {current_profile['grade']}\n"
        f"🎯 Цель обучения: {current_profile['goal']}\n"
        f"🌍 Часовой пояс: {current_profile['timezone']}\n"
        f"📱 Контакт: {current_profile['contact']}\n\n"
        "Выберите поле для редактирования:"
    )

    await update.message.reply_text(
        profile_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    # Remove keyboard
    await update.message.reply_text(
        "🔧 Выберите поле для редактирования...",
        reply_markup=ReplyKeyboardRemove()
    )

async def save_field_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE, field_name: str, new_value, field_display_name: str):
    """Save the edited field and return to main menu"""
    user_id = update.effective_user.id
    current_profile = context.user_data['current_profile']

    # Update the field
    current_profile[field_name] = new_value

    # Save to database
    save_user_profile(user_id, current_profile)

    await update.message.reply_text(
        f"✅ {field_display_name} успешно обновлен!\n\n"
        f"Новое значение: **{new_value}**\n\n"
        f"Возвращаемся в главное меню...",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown'
    )

    # Clear user data and return to main menu
    context.user_data.clear()
    from handlers.profile import send_main_menu
    await send_main_menu(update, context)

async def go_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go to main menu"""
    context.user_data.clear()
    await update.message.reply_text(
        "🏠 Возвращаемся в главное меню...",
        reply_markup=ReplyKeyboardRemove()
    )
    from handlers.profile_handler import send_main_menu
    await send_main_menu(update, context)

async def cancel_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel profile editing"""
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Редактирование профиля отменено.",
        reply_markup=ReplyKeyboardRemove()
    )
    from handlers.profile_handler import send_main_menu
    await send_main_menu(update, context)

def edit_profile_conv_handler():
    """Create the conversation handler for profile editing"""
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Text(["🛠️ Редактировать профиль"]), edit_profile_start)],
        states={
            EDIT_FIELD_SELECT: [CallbackQueryHandler(handle_field_selection)],
            EDIT_PARENT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_parent_name)],
            EDIT_CHILD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_child_name)],
            EDIT_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_age)],
            EDIT_GRADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_grade)],
            EDIT_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_goal)],
            EDIT_TIMEZONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_timezone)],
            EDIT_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_contact)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_edit),
            MessageHandler(filters.Text(["❌ Отмена", "🏠 Главное меню"]), cancel_edit)
        ],
        per_user=True
    )