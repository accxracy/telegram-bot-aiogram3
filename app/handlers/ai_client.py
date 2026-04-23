from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from io import BytesIO
import logging

from app.data.neuro import Neuro
from app.data.connection import (
    save_neuro_history, get_recent_context, check_user_limit,
    save_user_usage, save_model, get_model
)
from app.keyboards import get_main_menu, get_help_menu, get_neuro_chat_menu, keyboard_models
from app.states import NeuroState, Solve_By_Photo
from app.metrics import REQUESTS_TOTAL, GEMINI_REQUESTS, GEMINI_LATENCY
from app.utils import build_context_prompt

router = Router()

@router.callback_query(F.data == "exit_neuro")
async def exit_neuro(callback: CallbackQuery, state: FSMContext):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await state.clear()

    user = callback.from_user
    user_link = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

    await callback.message.edit_text(
        f"👋 Привет, {user_link}! Я бот-помощник по физике и математике!",
        reply_markup=get_main_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "menu_neuro")
async def process_neuro(callback: CallbackQuery, state: FSMContext):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await state.clear()
    model = await get_model(callback.from_user.id)
    await callback.message.edit_text(
        f"🤖 Нейро-мод. Модель: {model}",
        reply_markup=get_help_menu()
    )
    await state.set_state(NeuroState.waiting_for_prompt)

@router.message(NeuroState.waiting_for_prompt, F.text)
async def neuro_prompt(message: Message, state: FSMContext):
    model = await get_model(message.from_user.id)
    wait_msg = await message.answer("🧠 Думаю...", reply_markup=get_neuro_chat_menu())

    has_limit = await check_user_limit(message.from_user.id, limit=20)
    if not has_limit:
        await wait_msg.edit_text(
            "❌ <b>Дневной лимит исчерпан!</b>\nТы задал уже 20 вопросов за сегодня. Возвращайся завтра или очисти историю.",
            reply_markup=get_help_menu()
        )
        return

    try:
        history_rows = await get_recent_context(message.from_user.id, limit=3)
        final_prompt = build_context_prompt(history_rows, message.text)
        with GEMINI_LATENCY.time():
            ai = Neuro(model_name=model)

            answer = await ai.make_response(final_prompt)
        GEMINI_REQUESTS.labels(status='success').inc()
        answer = answer[:4000]

        await save_neuro_history(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            prompt=message.text,
            answer=answer,
            model="gemini"
        )

        await save_user_usage(
            telegram_id=message.from_user.id
        )

        await wait_msg.edit_text(answer, reply_markup=get_neuro_chat_menu())
    except Exception as ex:
        GEMINI_REQUESTS.labels(status='error').inc()
        logging.exception(f"Ошибка запроса: {ex}")
        await wait_msg.edit_text(
            f"❌ Ошибка при обращении к нейросети. Попробуй еще раз позже.",
            reply_markup=get_neuro_chat_menu()
        )

@router.callback_query(F.data == "photo_solve")
async def ask_for_photo(callback: CallbackQuery, state: FSMContext):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text(
    "📸 Отправь мне фотографию задачи.\n\n",
    parse_mode="HTML",
    reply_markup=get_help_menu()
    )
    await state.set_state(Solve_By_Photo.wait_photo)


@router.message(Solve_By_Photo.wait_photo, F.photo)
async def process_photo_task(message: Message, state: FSMContext, bot):
    model = await get_model(message.from_user.id)
    REQUESTS_TOTAL.labels(type='photo').inc()
    loading_msg = await message.answer("🧠 Анализирую картинку... Это может занять пару секунд. (/cancel для отмены)")
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    downloaded_file = BytesIO()
    await bot.download_file(file.file_path, downloaded_file)
    image_bytes = downloaded_file.getvalue()

    try:
        with GEMINI_LATENCY.time():
            ai_client = Neuro(model)
            answer = await ai_client.solve_from_photo(image_bytes)
            await loading_msg.edit_text(answer, parse_mode="Markdown", reply_markup=get_help_menu())
            try:
                await loading_msg.edit_text(answer, parse_mode="Markdown", reply_markup=get_help_menu())
            except TelegramBadRequest:
                await loading_msg.edit_text(answer, parse_mode=None, reply_markup=get_help_menu())
            GEMINI_REQUESTS.labels(status='success').inc()
    except Exception as ex:
        await loading_msg.edit_text(f"❌ Не смог распознать задачу.", reply_markup=get_help_menu())
        logging.error(ex)
        GEMINI_REQUESTS.labels(status='error').inc()
    finally:
        await state.clear()


@router.message(Solve_By_Photo.wait_photo, F.text)
async def wrong_format_in_photo_state(message: Message, state: FSMContext):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await message.answer("📸 Я жду именно фотографию задачи! \nЕсли передумал, нажми /cancel")

@router.callback_query(F.data == "menu_choose_neuro")
async def neuro_choose(callback: CallbackQuery):
    await callback.message.edit_text('Выберите модель: ', reply_markup=keyboard_models())


@router.callback_query(F.data.startswith("set_model"))
async def set_model(callback: CallbackQuery):
    model = callback.data.split("_")[2]
    model_name = f"gemini-{model}"

    await save_model(callback.from_user.id, model_name)

    await callback.message.edit_text("Модель успешно обновлена! Теперь AI будет отвечать через неё.", reply_markup=get_help_menu())