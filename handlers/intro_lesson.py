from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters,
)
from config import CHANNEL_ID
from handlers.profile import send_main_menu
import re

# Этапы анкеты
(
    PARENT_NAME, CHILD_NAME, AGE, CLASS,
    GOAL, TIMEZONE_SELECT, TIMEZONE_MANUAL,
    SUBJECT_SELECTION, CONTACT_METHOD, CONTACT_INPUT, 
    CONFIRM, EDIT_SELECT, EDIT_FIELD
) = range(13)


CONFIRM_REPLY = ReplyKeyboardMarkup(
    [["✅ Подтвердить", "✏️ Изменить", "⬅️ Назад"]],
    resize_keyboard=True,
    one_time_keyboard=True
)

TIMEZONES = ["GMT+3", "GMT+4", "GMT+5"]
TIMEZONE_REPLY = ReplyKeyboardMarkup(
    [[tz] for tz in TIMEZONES] + [["🌤️ Ввести вручную"]],
    resize_keyboard=True,
    one_time_keyboard=True
)

CONTACT_METHOD_REPLY = ReplyKeyboardMarkup(
    [["Telegram", "WhatsApp"]],
    resize_keyboard=True,
    one_time_keyboard=True
)

FIELDS = [
    ("parent_name", "👨‍👩‍👧‍👦 Введите ФИО родителя:"),
    ("child_name", "🧒 Введите ФИО ребёнка:"),
    ("age", "🎂 Возраст ребёнка:"),
    ("school_class", "🏫 В каком классе ребёнок?"),
    ("goal", "🎯 Какая цель обучения?"),
    ("timezone", "🌍 Укажите часовой пояс:"),
    ("subjects", "📘 Выберите предметы из прайс-листа:")
]

# Далее идут функции delete_all_messages, save_message, валидации, обработчики и get_intro_lesson_handler как в предыдущем коде. Их нужно вставить сюда без изменений.

# Чтобы не перегружать поле, вставим только заголовок. Продолжение — в следующем сообщении, если нужно полностью разбить код на части для редактирования.
async def delete_all_messages(context):
    for key in ['bot_messages', 'user_messages']:
        for msg in context.user_data.get(key, []):
            try:
                await msg.delete()
            except:
                pass
        context.user_data[key] = []

def save_message(context, message, who="bot"):
    key = 'bot_messages' if who == "bot" else 'user_messages'
    context.user_data.setdefault(key, []).append(message)

# Валидация

def is_text_only(value):
    return bool(re.match(r"^[А-Яа-яA-Za-z\s\-]+$", value))

def is_age_valid(value):
    return value.isdigit() and 1 <= int(value) <= 18

def is_class_valid(value):
    return value.isdigit() and 1 <= int(value) <= 7

def is_telegram_username(value):
    return value.startswith("@") and len(value) > 1

def is_whatsapp_number(value):
    return bool(re.match(r"^\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$", value))

# Обработчики

async def start_intro_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_all_messages(context)
    context.user_data.clear()

    msg = await update.message.reply_text(FIELDS[0][1], reply_markup=ReplyKeyboardRemove())
    save_message(context, msg)
    save_message(context, update.message, "user")
    return PARENT_NAME

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE, field_index: int):
    save_message(context, update.message, "user")
    value = update.message.text
    key, prompt = FIELDS[field_index]

    if field_index == PARENT_NAME or field_index == CHILD_NAME:
        if not is_text_only(value):
            msg = await update.message.reply_text("❌ Введите только текст (без цифр):")
            save_message(context, msg)
            return field_index
    elif field_index == AGE:
        if not is_age_valid(value):
            msg = await update.message.reply_text("❌ Возраст должен быть числом от 1 до 18:")
            save_message(context, msg)
            return field_index
    elif field_index == CLASS:
        if not is_class_valid(value):
            msg = await update.message.reply_text("❌ Класс должен быть числом от 1 до 7:")
            save_message(context, msg)
            return field_index

    context.user_data[key] = value
    await delete_all_messages(context)

    if field_index == GOAL:
        msg = await update.message.reply_text("🌍 Выберите часовой пояс:", reply_markup=TIMEZONE_REPLY)
        save_message(context, msg)
        return TIMEZONE_SELECT

    msg = await update.message.reply_text(FIELDS[field_index + 1][1], reply_markup=ReplyKeyboardRemove())
    save_message(context, msg)
    return field_index + 1

async def handle_timezone_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_message(context, update.message, "user")
    tz = update.message.text
    if tz == "🔤 Ввести вручную":
        msg = await update.message.reply_text("Введите ваш часовой пояс (например, GMT+6):", reply_markup=ReplyKeyboardRemove())
        save_message(context, msg)
        return TIMEZONE_MANUAL
    else:
        context.user_data['timezone'] = tz
        await delete_all_messages(context)
        context.user_data["subjects"] = []
        return await handle_subject_selection(update, context)

async def handle_timezone_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_message(context, update.message, "user")
    context.user_data['timezone'] = update.message.text
    await delete_all_messages(context)
    context.user_data["subjects"] = []
    return await handle_subject_selection(update, context)

async def handle_subject_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subjects = context.bot_data.get("price_list", ["Математика", "Русский", "Английский"])
    user_input = update.message.text if update.message else None

    if user_input:
        save_message(context, update.message, "user")
        if user_input == "✅ Готово":
            if not context.user_data['subjects']:
                msg = await update.message.reply_text("❌ Выберите хотя бы один предмет.")
                save_message(context, msg)
                return SUBJECT_SELECTION
            msg = await update.message.reply_text("📱 Выберите контактный способ:", reply_markup=CONTACT_METHOD_REPLY)
            save_message(context, msg)
            return CONTACT_METHOD
        elif user_input in context.user_data['subjects']:
            context.user_data['subjects'].remove(user_input)
        elif user_input in subjects:
            if len(context.user_data['subjects']) >= 3:
                msg = await update.message.reply_text("❌ Можно выбрать не более 3 предметов.")
                save_message(context, msg)
                return SUBJECT_SELECTION
            context.user_data['subjects'].append(user_input)

    await delete_all_messages(context)
    buttons = [[KeyboardButton(s)] for s in subjects]
    buttons.append([KeyboardButton("✅ Готово")])
    selected = ", ".join(context.user_data.get("subjects", [])) or "—"
    msg = await update.message.reply_text(
        f"📘 Выберите предметы из прайс-листа:\n\nВы выбрали: {selected}",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
    save_message(context, msg)
    return SUBJECT_SELECTION

# Остальные обработчики остаются без изменений

async def handle_contact_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_message(context, update.message, "user")
    method = update.message.text
    context.user_data['contact_method'] = method

    if method == "Telegram":
        username = update.effective_user.username
        if username:
            contact = f"@{username}"
            context.user_data['contact'] = contact

            summary = "\n".join([
                f"{FIELDS[i][1]} {', '.join(context.user_data[FIELDS[i][0]]) if isinstance(context.user_data[FIELDS[i][0]], list) else context.user_data[FIELDS[i][0]]}"
                for i in range(len(FIELDS))
            ])
            summary += f"\n📞 Способ связи: {context.user_data.get('contact_method', '—')} ({context.user_data.get('contact', '—')})"

            msg = await update.message.reply_text(f"📋 Проверьте ваши ответы:\n\n{summary}", reply_markup=CONFIRM_REPLY)
            save_message(context, msg)
            return CONFIRM
        else:
            msg = await update.message.reply_text(
                "❌ У вас не установлен Telegram username. Пожалуйста, выберите другой способ связи (например, WhatsApp).",
                reply_markup=CONTACT_METHOD_REPLY
            )
            save_message(context, msg)
            return CONTACT_METHOD

    elif method == "WhatsApp":
        msg = await update.message.reply_text(
            "Введите WhatsApp номер в формате +7 999 999 99 99:",
            reply_markup=ReplyKeyboardRemove()
        )
        save_message(context, msg)
        return CONTACT_INPUT

    else:
        msg = await update.message.reply_text(
            "❌ Пожалуйста, выберите способ из списка ниже:",
            reply_markup=CONTACT_METHOD_REPLY
        )
        save_message(context, msg)
        return CONTACT_METHOD


async def handle_contact_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_message(context, update.message, "user")
    method = context.user_data['contact_method']
    contact = update.message.text
    if method == "Telegram":
        if not is_telegram_username(contact):
            msg = await update.message.reply_text("❌ Введите корректный Telegram username, начиная с @:")
            save_message(context, msg)
            return CONTACT_INPUT
    elif method == "WhatsApp":
        if not is_whatsapp_number(contact):
            msg = await update.message.reply_text("❌ Введите номер в формате +7 999 999 99 99:")
            save_message(context, msg)
            return CONTACT_INPUT
    context.user_data['contact'] = contact

    summary = "\n".join([
        f"{FIELDS[i][1]} {', '.join(context.user_data[FIELDS[i][0]]) if isinstance(context.user_data[FIELDS[i][0]], list) else context.user_data[FIELDS[i][0]]}" for i in range(len(FIELDS))
    ])
    summary += f"\n📞 Способ связи: {context.user_data.get('contact_method', '—')} ({context.user_data.get('contact', '—')})"

    msg = await update.message.reply_text(f"📋 Проверьте ваши ответы:\n\n{summary}", reply_markup=CONFIRM_REPLY)
    save_message(context, msg)
    return CONFIRM

async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_message(context, update.message, "user")
    await delete_all_messages(context)
    text = update.message.text

    if text == "✅ Подтвердить":
        summary = "\n".join([
            f"{FIELDS[i][1]} {', '.join(context.user_data[FIELDS[i][0]]) if isinstance(context.user_data[FIELDS[i][0]], list) else context.user_data[FIELDS[i][0]]}" for i in range(len(FIELDS))
        ])
        summary += f"\n\n📞 Способ связи: {context.user_data.get('contact_method', '—')} ({context.user_data.get('contact', '—')})"

        await context.bot.send_message(chat_id=CHANNEL_ID, text=f"📩 Новая анкета:\n\n{summary}")
        msg = await update.message.reply_text("✅ Спасибо! Анкета отправлена.", reply_markup=ReplyKeyboardRemove())
        save_message(context, msg)
        context.user_data.clear()
        await send_main_menu(update, context)
        return ConversationHandler.END

    elif text == "⬅️ Назад":
        await send_main_menu(update, context)
        context.user_data.clear()
        return ConversationHandler.END

    elif text == "✏️ Изменить":
        msg = await update.message.reply_text("📝 Что вы хотите изменить?", reply_markup=EDIT_OPTIONS_REPLY)
        save_message(context, msg)
        return EDIT_SELECT

    else:
        msg = await update.message.reply_text("Пожалуйста, используйте кнопки ниже:", reply_markup=CONFIRM_REPLY)
        save_message(context, msg)
        return CONFIRM
    
async def handle_edit_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_message(context, update.message, "user")
    text = update.message.text

    match = re.match(r"^(\d+)\. ", text)
    if match:
        field_index = int(match.group(1)) - 1
        context.user_data['edit_field_index'] = field_index
        await delete_all_messages(context)

        if field_index == len(FIELDS) - 1:  # SUBJECT_SELECTION
            context.user_data['subjects'] = []
            return await handle_subject_selection(update, context)

        if field_index == 5:  # TIMEZONE_SELECT
            msg = await update.message.reply_text("🌍 Выберите часовой пояс:", reply_markup=TIMEZONE_REPLY)
            save_message(context, msg)
            return TIMEZONE_SELECT

        msg = await update.message.reply_text(FIELDS[field_index][1], reply_markup=ReplyKeyboardRemove())
        save_message(context, msg)

        return EDIT_FIELD
    else:
        msg = await update.message.reply_text("❌ Пожалуйста, выберите корректный пункт.", reply_markup=EDIT_OPTIONS_REPLY)
        save_message(context, msg)
        return EDIT_SELECT

async def handle_edit_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    field_index = context.user_data.get('edit_field_index')
    return await handle_text(update, context, field_index)

EDIT_OPTIONS_REPLY = ReplyKeyboardMarkup(
    [[f"{i + 1}. {FIELDS[i][1].strip('🧒👨‍👩‍👧‍👦🎂🏫🎯🌍📘:')}" for i in range(len(FIELDS))]],
    resize_keyboard=True,
    one_time_keyboard=True
)

async def cancel_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_message(context, update.message, "user")
    await delete_all_messages(context)
    context.user_data.clear()
    msg = await update.message.reply_text("❌ Анкета отменена.", reply_markup=ReplyKeyboardRemove())
    save_message(context, msg)
    await send_main_menu(update, context)
    return ConversationHandler.END

def get_intro_lesson_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("^🎓 Вводный урок$"), start_intro_lesson)],
        states={
            PARENT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: handle_text(u, c, PARENT_NAME))],
            CHILD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: handle_text(u, c, CHILD_NAME))],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: handle_text(u, c, AGE))],
            CLASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: handle_text(u, c, CLASS))],
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: handle_text(u, c, GOAL))],
            TIMEZONE_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_timezone_select)],
            TIMEZONE_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_timezone_manual)],
            SUBJECT_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_subject_selection)],
            CONTACT_METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_contact_method)],
            CONTACT_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_contact_input)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confirmation)],
            EDIT_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_select)],
            EDIT_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_field)],
        },
        fallbacks=[CommandHandler("cancel", cancel_intro)],
        per_user=True,
        per_chat=True,
    )