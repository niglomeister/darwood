
Техническое задание: Telegram-бот для онлайн-школы Формат: ЗВЯ (Заголовок — Вопрос — Ясный ответ) Версия: 1.8.3 | Подготовлено: Май 2025 Автор: Darwood & Евгений.М

1. 🚀 Приветствие и старт
В: Как пользователь начинает взаимодействие? О: Бот приветствует пользователя при первом запуске и предлагает нажать кнопку «🚀 Старт». Далее открывается Главное меню.

2. 🧑‍🎓 Главное меню (до создания профиля)
Кнопки:
👤 Мой профиль (обязательное создание)
🎓 Вводный урок
После создания профиля добавляются:
📚 Домашнее задание
📝 Записаться на урок
❌ Отменить урок
🔁 Перенести урок
🏅 Награды
🛠️ Редактировать профиль
ℹ️ Информацияi
🧑‍🏫 Связь с учителем

3. ℹ️ Информация
Доступна после создания профиля
Если не записан ни на один урок: «Сначала запишитесь на урок» + «🔙 Назад»
Если ученик записан:
Список всех уроков: 📆 Дата, ⏰ Время, 📘 Занятие, 💵 Стоимость
Общий подсчёт: количество + сумма
Кнопки оплаты: 💳 Оплатить ближайший, 💰 Оплатить все
После выбора:
Реквизиты, сумма, «✅ Я оплатил»
Указание комментария к оплате — ФИО
После подтверждения — урок «⏳ Ожидает подтверждения»
Админ вручную переводит в «✅ Оплаченные»
При неоплате:
У админа: «📌 Неоплаченные уроки» → ученик → список
Кнопка «📤 Напомнить об оплате» → сообщение ученику
Если за сутки не оплачено:
Урок отменяется, слот освобождается
Уведомление ученику и в канал учителя

4. 🧑‍🏫 Связь с учителем
Ученик:
💰 Вопросы об оплате
❓ Задать вопрос учителю
Админ:
💰 Вопросы об оплате
❓ Вопросы учеников
Отсутствие обращений → сообщение и «🔙 Назад»
При входящих — список тикетов (по ФИО)
Внутри: диалог, «🔙 Назад», «✅ Закрыть тикет»

5. 🧾 Создание профиля ученика
Шаги:
👨‍👩‍👧‍👦 ФИО родителя
🧒 ФИО ребёнка
🎂 Возраст
🏫 Класс
🎯 Цель обучения
🌍 Часовой пояс (+ ручной ввод)
📘 Занятия (из прайс-листа)
📱 Контакт (Telegram / WhatsApp)
Telegram → @username
WhatsApp → номер с валидацией
Если нет прайс-листа — сообщение об ожидании
После — сохранение данных

6. 🛠️ Редактирование профиля
«👤 Мой профиль» → показать все поля
«🛠️ Редактировать» → выбор поля
После — «✅ Подтвердить изменения»

7. 🎓 Вводный урок
Доступен без создания профиля
Те же вопросы, но без сохранения
После:
«✅ Подтвердить» → админу
«❌ Отменить» → сообщение
Кнопки «🔙 Назад» нет

8. 📝 Запись на урок
Выбор занятия (из профиля)
Выбор даты и времени
Подтверждение → «📌 Урок забронирован», уведомление админу
Появляется в «ℹ️ Информация»
Если не подтвержден за 5 минут — слот освобождается
Защита от двойного бронирования: занятые слоты скрываются

9. 🔁 Перенос / ❌ Отмена урока
Перенос:
Список будущих уроков → выбор нового времени
Подтверждение → обновление + уведомление админу
Отмена:
Удаление слота
Уведомление админу (ФИО и время)

10. 📚 Домашнее задание
Получение:
Показ по занятиям (текст/фото)
«📤 Отправить задание»
Отправка:
Прикрепить фото
Добавление/удаление
«✅ Подтвердить отправку»
Проверка:
Админ → «📩 Выполненные задания»
Фото + кнопки:
🎯 Оценить (1–5)
💬 Комментарий
Баллы добавляются к ученику
История:
Ученик → «📚 Проверенные задания»
Админ → «🗂️ Прошлые задания»

11. ⏰ Напоминание об уроке
За 1 час (учёт часового пояса)
Пример: «⏰ Через час в 15:00 у вас урок по Математике. Удачи!»

12. 💳 Оплата
Модель:
После записи — сумма + реквизиты
После «✅ Я оплатил» → «⏳ Ожидает подтверждения» → подтверждение вручную
Админ-вкладки:
«⏳ Ожидающие оплаты»
«✅ Оплаченные»
«📌 Неоплаченные»

13. 🏅 Награды
Цели, прогресс, «🎯 Выбрать»
Баллы сохраняются
Шкала обновляется при смене цели

14. 📊 Статистика (админ)
📋 Кол-во учеников
🏆 Топ по баллам
📩 Задания
📚 Уроки по датам и статусам
💸 Оплаты: суммы, фильтры, по ученикам

15. 🧰 Админ-панель
Кнопки:
👩‍🎓 Ученики
✏️ Задания
📩 Выполненные задания
🏅 Награды
📊 Статистика
📚 Уроки
🛟 Поддержка
💳 Реквизиты
📄 Прайс-лист
💳 Реквизиты:
Первый раз — ввод всех данных
Потом — «✏️ Редактировать» → выбор → подтверждение
📄 Прайс-лист:
При отсутствии — «➕ Добавить занятие»
Ввод:
📝 Название
💵 Цена
«✅ Подтвердить»
Далее — список, кнопки редактирования
Все оплаты используют прайс-лист

16. 📨 Сообщение ученику (админ)
Список учеников с уроками сегодня


Technical Specification: Telegram Bot for Online School Format: ZVY (Title - Question - Clear Answer) Version: 1.8.3 | Prepared: May 2025 Author: Darwood & Evgeny.M

1. 🚀 Welcome and Start
Q: How does the user start interacting? A: The bot welcomes the user upon first launch and prompts them to click the "🚀 Start" button. This opens the Main Menu.

2. 🧑‍🎓 Main menu (before creating a profile)
Buttons:
👤 My profile (must be created)
🎓 Introductory lesson
After creating a profile, the following are added:
📚 Homework
📝 Sign up for a lesson
❌ Cancel a lesson
🔁 Postpone a lesson
🏅 Rewards
🛠️ Edit a profile
ℹ️ Information
🧑‍🏫 Teacher contact

3. ℹ️ Information
Available after creating a profile
If not enrolled in any lessons: "First enroll in a lesson" + "🔙 Back"
If the student is enrolled:
List of all lessons: 📆 Date, ⏰ Time, 📘 Lesson, 💵 Cost
Total count: quantity + amount
Payment buttons: 💳 Pay for the nearest lesson, 💰 Pay for all lessons
After selection:
Details, amount, "✅ I have paid"
 Payment comment, full name
 After confirmation, the lesson is "⏳ Waiting for confirmation"
The admin manually transfers it to "✅ Paid"
If payment is not made:
Admin: "📌 Unpaid lessons" → student → list
 "📤 Remind me to pay" button → message to the student
 If payment is not made within 24 hours:
 The lesson is canceled, and the slot is released
 Notification to the student and to the teacher's channel

4. 🧑‍🏫 Connection with the teacher
Student:
💰 Payment questions
❓ Ask a question to the teacher
Admin:
💰 Payment questions
❓ Student questions
No requests → message and "🔙 Back"
When incoming - list of tickets (by name)
Inside: dialogue, "🔙 Back", "✅ Close ticket"

5. 🧾 Creating a student profile
Steps:
👨‍👩‍👧‍👦 Parent's name
🧒 Child's name
🎂 Age
🏫 Grade
🎯 Learning goal
🌍 Time zone (+ manual input)
📘 Classes (from the price list)
📱 Contact (Telegram / WhatsApp)
Telegram → @username
WhatsApp → validated number
If there is no price list, a waiting message will appear
After that, the data will be saved

6. 🛠️ Profile editing
«👤 My profile» → show all fields
«🛠️ Edit» → select a field
After — «✅ Confirm changes»

7. 🎓 Introduction lesson
Available without creating a profile
The same questions, but without saving
After:
«✅ Confirm» → admin
«❌ Cancel» → message
There is no «🔙 Back» button

8. 📝 Book a lesson
Select a lesson (from the profile)
Select a date and time
Confirm → "📌 Lesson booked", notify the admin
Appears in "ℹ️ Information"
If not confirmed within 5 minutes, the slot is released
Double booking protection: occupied slots are hidden

9. 🔁 Reschedule / ❌ Cancel a lesson
Reschedule:
List of upcoming lessons → select a new time
Confirm → update + notify the admin
Cancel:
Delete slot
Notify admin (name and time)

10. 📚 Homework
Receive:
Show by classes (text/photo)
«📤 Send task»
Send:
Attach photo
Add/delete
«✅ Confirm sending»
Check:
Admin → «📩 Completed tasks»
Photo + buttons:
🎯 Rate (1–5)
💬 Comment
Points are added to the student
History:
Student → "📚 Verified assignments"
Admin → "🗂️ Past assignments"

11. ⏰ Lesson reminder
1 hour in advance (time zone)
Example: "⏰ In one hour, at 15:00, you have a math lesson. Good luck!"

12. 💳 Payment
Model:
After recording, the amount and details are displayed
After "✅ I paid" → "⏳ Waiting for confirmation" → manual confirmation
Admin tabs:
"⏳ Waiting for payment"
"✅ Paid"
"📌 Unpaid"

13. 🏅 Rewards
Goals, progress, "🎯 Select"
Points are saved
The scale is updated when the goal is changed

14. 📊 Statistics (admin)
📋 Number of students
🏆 Top by points
📩 Tasks
📚 Lessons by dates and statuses
💸 Payments: amounts, filters, by students

15. 🧰 Admin panel
Buttons:
👩‍🎓 Students
✏️ Tasks
📩 Completed tasks
🏅 Rewards
📊 Statistics
📚 Lessons
🛟 Support
💳 Details
📄 Price list
💳 Details:
The first time - enter all data
Then - "✏️ Edit" → selection → confirmation
📄 Price list:
If absent - "➕ Add lesson"
Input:
📝 Name
💵 Price
«✅ Confirm»
Next - list, edit buttons
All payments use the price list

16. 📨 Message to the student (admin)
