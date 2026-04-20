from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging
from app.data.connection import get_user_neuro_history, delete_user_neuro_history
from app.keyboards import get_help_menu, get_main_menu
from app.states import FeedBack
from app.config import ADMIN_ID
from app.keyboards import HELP_TEXT

router = Router()

@router.message(Command("history"))
async def print_history(message: Message):

    usr = message.from_user.id
    try:
        history = await get_user_neuro_history(usr)
        if not history:
            await message.answer("История пуста", reply_markup=get_help_menu())
            return

        text = "<b>История запросов:</b>\n\n"

        for i, row in enumerate(history, start=1):
            row = dict(row)

            prompt = row["prompt"][:100]
            answer = row["answer"][:200]

            text += (
                f"<b>{i}.</b> <b>Модель:</b> <code>{row['model']}</code>\n"
                f"<b>Запрос:</b> {prompt}\n"
                f"<b>Ответ:</b> {answer}\n"
                f"<b>Дата:</b> {row['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
            )

        await message.answer(text, reply_markup=get_help_menu())
    except Exception as ex:
        logging.exception(f"Ошибка истории: {ex}")
        await message.answer(f"❌ Ошибка при обращении к БД. Попробуй еще раз позже.")

@router.message(Command("clear_history"))
async def clear_history(message: Message):
    usr = message.from_user.id
    try:
        await delete_user_neuro_history(usr)
        await message.answer("🧹 Твоя история запросов успешно очищена!", reply_markup=get_help_menu())
    except Exception as ex:
        logging.exception(f"Ошибка при удалении истории: {ex}")
        await message.answer("❌ Произошла ошибка. Попробуй позже.")


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=get_main_menu())

@router.message(Command("feedback"))
async def feedback_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FeedBack.waiting_for_feedback)
    await message.answer("✅ Напишите ваш отзыв (/cancel для отмены):")

@router.message(FeedBack.waiting_for_feedback, F.text)
async def feedback(message: Message, state: FSMContext, bot):
    await bot.send_message(
        int(ADMIN_ID),
        f"📩 <b>Новый фидбек</b>\n\n"
        f"👤 От: {message.from_user.full_name}\n"
        f"🆔 ID: <code>{message.from_user.id}</code>\n"
        f"📎 Username: @{message.from_user.username if message.from_user.username else 'нет'}\n\n"
        f"💬 {message.text}"
    )
    await state.clear()
    await message.answer(text="Спасибо!", reply_markup=get_help_menu())

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user = message.from_user
    user_link = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

    await message.answer(
        f"👋 Привет, {user_link}! Я бот-помощник по физике и математике!",
        reply_markup=get_main_menu()
    )

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(HELP_TEXT, reply_markup=get_help_menu())