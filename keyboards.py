from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Common
BTN_CANCEL = "✖️ Отмена"
BTN_BACK = "⬅️ Назад"
BTN_MAIN_MENU = "🏠 В главное меню"

# Agent main
BTN_NEW = "▶️ Новый опрос (квартира)"
BTN_HELP = "ℹ️ Помощь"
BTN_MY_STATS = "📊 Сводка за смену"

# Admin main
BTN_ADMIN = "🛠 Админ-меню"
BTN_ADMIN_LOGIN = "🔐 Админ-вход"
BTN_ADMIN_LOGOUT = "🚪 Выйти из админа"
BTN_EXPORT = "📤 Экспорт XLSX"
BTN_ADMIN_HELP = "ℹ️ Справка админа"
BTN_ADMIN_STATS_ALL = "📈 Сводка по всем"  # NEW

# Repeat touch
BTN_PRIMARY = "Первичное касание"
BTN_SECONDARY = "Повторное касание"

# Talk status
BTN_NO_ONE = "Никого нет"
BTN_REFUSAL = "Отказ от общения"
BTN_CONSENT = "Согласие на общение"

# Flyer method
BTN_HAND = "Да, на руки"
BTN_MAILBOX = "Да, в почтовый ящик"
BTN_NO = "Нет"

# Yes/No generic
BTN_YES = "Да"
BTN_NOT = "Нет"

# Photos
BTN_SKIP = "Пропустить"

# Finish
BTN_FINISH = "✅ Завершить опрос"
BTN_ADD_MORE = "➕ Добавить ещё одного избирателя"

# Export ranges
BTN_EXP_TODAY = "Сегодня"
BTN_EXP_7 = "7 дней"
BTN_EXP_30 = "30 дней"
BTN_EXP_ALL = "Всё"

def kb_main(is_admin: bool) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=BTN_NEW)],
        [KeyboardButton(text=BTN_MY_STATS)],
        [KeyboardButton(text=BTN_HELP)],
    ]
    if is_admin:
        keyboard.append([KeyboardButton(text=BTN_ADMIN)])
    else:
        keyboard.append([KeyboardButton(text=BTN_ADMIN_LOGIN)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def kb_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_CANCEL)]],
        resize_keyboard=True
    )

def kb_repeat_touch() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_PRIMARY)],
            [KeyboardButton(text=BTN_SECONDARY)],
            [KeyboardButton(text=BTN_CANCEL)],
        ],
        resize_keyboard=True
    )

def kb_status() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_NO_ONE)],
            [KeyboardButton(text=BTN_REFUSAL)],
            [KeyboardButton(text=BTN_CONSENT)],
            [KeyboardButton(text=BTN_CANCEL)],
        ],
        resize_keyboard=True
    )

def kb_flyer_method() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_HAND)],
            [KeyboardButton(text=BTN_MAILBOX)],
            [KeyboardButton(text=BTN_NO)],
            [KeyboardButton(text=BTN_CANCEL)],
        ],
        resize_keyboard=True
    )

def kb_yes_no() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_YES), KeyboardButton(text=BTN_NOT)],
            [KeyboardButton(text=BTN_CANCEL)],
        ],
        resize_keyboard=True
    )

def kb_skip_or_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_SKIP)], [KeyboardButton(text=BTN_CANCEL)]],
        resize_keyboard=True
    )

def kb_finish_or_add() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_FINISH)],
            [KeyboardButton(text=BTN_ADD_MORE)],
            [KeyboardButton(text=BTN_MAIN_MENU)]
        ],
        resize_keyboard=True
    )

def kb_admin_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ADMIN_STATS_ALL)],   # NEW first row
            [KeyboardButton(text=BTN_EXPORT)],
            [KeyboardButton(text=BTN_ADMIN_HELP)],
            [KeyboardButton(text=BTN_ADMIN_LOGOUT)],
            [KeyboardButton(text=BTN_MAIN_MENU)]
        ],
        resize_keyboard=True
    )

def kb_export_ranges() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_EXP_TODAY), KeyboardButton(text=BTN_EXP_7)],
            [KeyboardButton(text=BTN_EXP_30), KeyboardButton(text=BTN_EXP_ALL)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )

def remove() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
