from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.math_topics import MATH_TOPICS
from data.topics import TOPICS



class TopicAction(CallbackData, prefix="ta"):
  topic: str
  action: str


HELP_TEXT = """
🤖 <b>Бот-тренажёр | Физика и Математика</b>

Выберите раздел с помощью кнопок ниже.

🎓 <b>Основные разделы:</b>
• <b>Теория:</b> <i>конспекты и правила по темам</i>
• <b>Формулы:</b> <i>удобная шпаргалка</i>
• <b>Теоремы:</b> <i>ключевые доказательства</i>
• <b>Задачи:</b> <i>генератор для практики и подготовки</i>

👤 <b>Профиль и AI:</b>
• <b>Профиль:</b> <i>статистика решённых задач</i>
• <b>Нейро-режим:</b> <i>задать вопрос Gemini 2.0</i>

⚙️ <b>Команды:</b>
<code>/history</code> — <i>история ваших запросов к AI</i>
<code>/clear_history</code> — <i>очистить историю</i>
<code>/feedback</code> — <i>связь с автором</i>

📊 <b>Лимит запросов к AI:</b> 20 в день
<i>(обновляется в 00:00 по МСК)</i>

<i>⚠️ Важно: Бот работает на энтузиазме, кофе и бесплатных API. Если нейросеть устала и ушла пить чай (выдала ошибку) — не ругайся, просто подожди пару минут. Базовый функционал тренажёра работает бесперебойно даже без ИИ! 🛠</i>
"""


def get_main_menu() -> InlineKeyboardMarkup:
 kb = [
  [InlineKeyboardButton(text="📝 Задачи(источник: sdamgia)", callback_data="menu_tasks")],
  [InlineKeyboardButton(text="📐 Математика", callback_data="menu_mathematics")],
  [InlineKeyboardButton(text="🧑‍🔬 Физика", callback_data="menu_physics")],
  [InlineKeyboardButton(text="🤖 Нейросеть", callback_data="menu_neuro")],
  [InlineKeyboardButton(text="👤Профиль", callback_data="menu_profile")],
  [InlineKeyboardButton(text="📚 Полезные материалы", callback_data="menu_useful_materials")],
  [InlineKeyboardButton(text="💡 О боте", callback_data="menu_help")],

 ]
 return InlineKeyboardMarkup(inline_keyboard=kb)

def get_help_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text='🔙 Главная', callback_data="menu_back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_topics_menu_physics() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    PHYSICS_TOPICS = TOPICS.keys()

    for topic in PHYSICS_TOPICS:
        builder.button(
            text=f"{topic}",
            callback_data=TopicAction(topic=topic, action="menu").pack()
        )

    builder.button(text="🔙 Главная", callback_data="menu_back_to_main")
    builder.adjust(1)
    return builder.as_markup()

def get_action_menu_physics(topic_name) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📚 Теория",
        callback_data=TopicAction(topic=topic_name, action="theory").pack()
    )
    builder.button(
        text="🧮 Формулы",
        callback_data=TopicAction(topic=topic_name, action="formulas").pack()
    )
    builder.button(
        text="💡 Подсказки",
        callback_data=TopicAction(topic=topic_name, action="hints").pack()
    )

    builder.button(text="🔙 К списку тем", callback_data="menu_physics")

    builder.adjust(2, 1, 1)
    return builder.as_markup()


def get_topics_menu_mathematics() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    topics = MATH_TOPICS.keys()

    for topic in topics:
        builder.button(
            text=f"{topic}",
            callback_data=TopicAction(topic=topic, action="menu_math").pack()
        )

    builder.button(text="🔙 Главная", callback_data="menu_back_to_main")
    builder.adjust(1)
    return builder.as_markup()


def get_action_menu_mathematics(topic_name) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📚 Теоремы",
        callback_data=TopicAction(topic=topic_name, action="theorems").pack()
    )
    builder.button(
        text="🧮 Формулы",
        callback_data=TopicAction(topic=topic_name, action="formulas_mathematics").pack()
    )


    builder.button(text="🔙 К списку тем", callback_data="menu_mathematics")

    builder.adjust(2, 1, 1)
    return builder.as_markup()


def get_neuro_chat_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🔙 Выйти из нейро-режима", callback_data="exit_neuro")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_random_task() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🎲 Сгенерировать(Математика)", callback_data="generate_task_math")],
        [InlineKeyboardButton(text="🎲 Сгенерировать(Физика)", callback_data="generate_task_physics")],
        [InlineKeyboardButton(text="🔙 Главная", callback_data="menu_back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def task_generator(task_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅", callback_data=f"task_done_{task_id}")
    builder.button(text="❌", callback_data=f"task_failed_{task_id}")

    builder.button(text="🎲 Перегенерация", callback_data="menu_tasks")

    builder.button(text="🧠 AI Объяснение", callback_data=f"ai_explain_{task_id}")
    builder.button(text="🔙 Главная", callback_data="menu_back_to_main")

    builder.adjust(2, 1, 1)
    return builder.as_markup()


def get_list_materials() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📚 Официально (ФИПИ)", callback_data="mat_fipi")
    builder.button(text="📐 YouTube: Математика", callback_data="mat_youtube_math")
    builder.button(text="🧲 YouTube: Физика", callback_data="mat_youtube_phys")
    builder.button(text="🌐 Полезные сайты", callback_data="mat_sites")
    builder.button(text="🔙 Главная", callback_data="menu_back_to_main")

    builder.adjust(1, 2, 1)
    return builder.as_markup()

def get_back_to_materials() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data="menu_useful_materials")

    builder.adjust(1)
    return builder.as_markup()