from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
import logging

from app.keyboards import (
    get_main_menu, get_help_menu, HELP_TEXT, TopicAction,
    get_topics_menu_physics, get_action_menu_physics,
    get_topics_menu_mathematics, get_action_menu_mathematics,
    get_list_materials, get_back_to_materials
)
from app.metrics import REQUESTS_TOTAL
from app.data.math_topics import MATH_TOPICS
from app.data.topics import TOPICS
from app.data.materials import MATERIALS

router = Router()


@router.callback_query(F.data == "menu_help")
async def process_help_menu(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text(
        HELP_TEXT,
        reply_markup=get_help_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "menu_back_to_main")
async def process_back_to_main(callback: CallbackQuery, state: FSMContext):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await state.clear()
    user = callback.from_user
    user_link = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    await callback.message.edit_text(
        f"👋 Привет, {user_link}! Я бот-помощник по физике и математике!",
        reply_markup=get_main_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "menu_physics")
async def process_physics_menu(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text(
        "Выберите раздел физики:",
        reply_markup=get_topics_menu_physics()
    )
    await callback.answer()


@router.callback_query(F.data == "menu_mathematics")
async def process_mathematics_menu(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text(
        "Выберите раздел математики:",
        reply_markup=get_topics_menu_mathematics()
    )
    await callback.answer()


@router.callback_query(TopicAction.filter())
async def process_topic_action(callback: CallbackQuery, callback_data: TopicAction):
    REQUESTS_TOTAL.labels(type='callback').inc()
    current_topic = callback_data.topic
    action = callback_data.action
    try:
        if action == "menu_math":
            await callback.message.edit_text(
                f"Раздел: {current_topic}\nЧто именно тебя интересует?",
                reply_markup=get_action_menu_mathematics(current_topic)
            )

        elif action == "th":
            theorems = MATH_TOPICS[current_topic]['theorems']
            await callback.message.edit_text(
                theorems,
                reply_markup=get_action_menu_mathematics(current_topic)
            )

        elif action == "f_m":
            formulas = MATH_TOPICS[current_topic]['formulas']
            await callback.message.edit_text(
                formulas,
                reply_markup=get_action_menu_mathematics(current_topic)
            )

        elif action == "menu":
            await callback.message.edit_text(
                f"Раздел: {current_topic}\nЧто именно тебя интересует?",
                reply_markup=get_action_menu_physics(current_topic)
            )

        elif action == "theory":
            theory_text = TOPICS[current_topic]['theory']
            await callback.message.edit_text(
                theory_text,
                reply_markup=get_action_menu_physics(current_topic)
            )

        elif action == "formulas":
            await callback.message.edit_text(
                TOPICS[current_topic]['formulas'],
                reply_markup=get_action_menu_physics(current_topic)
            )

        elif action == "hints":
            hints_text = ""
            hints = TOPICS[current_topic]['hints']
            for title, text in hints.items():
                hints_text += f"💡 <b>{title}</b>\n{text}\n\n"
            await callback.message.edit_text(
                hints_text,
                reply_markup=get_action_menu_physics(current_topic)
            )

        await callback.answer()
    except TelegramBadRequest as ex:
        if "message is not modified" in str(ex):
            pass
        else:
            logging.exception(f"Ошибка при обработке callback: {ex}")

@router.callback_query(F.data == "menu_useful_materials")
async def useful_materials(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text('Выберите категорию: ', reply_markup=get_list_materials())

@router.callback_query(F.data.startswith("mat_"))
async def mats(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    category_key = callback.data.replace("mat_", "")

    items = MATERIALS.get(category_key, [])

    if not items:
        await callback.answer("Материалы пока не добавлены.", show_alert=True)
        return

    titles = {
        "fipi": "📚 Официальные ресурсы ФИПИ:",
        "youtube_math": "📐 YouTube: Математика:",
        "youtube_phys": "🧲 YouTube: Физика:",
        "sites": "🌐 Полезные сайты и тренажеры:"
    }

    header = titles.get(category_key, "📌 Полезные материалы:")
    text = f"<b>{header}</b>\n\n"

    for item in items:
        text += f"🔹 <a href='{item['url']}'>{item['title']}</a>\n"
        text += f"<i>{item['desc']}</i>\n\n"

    await callback.message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=get_back_to_materials()
    )
