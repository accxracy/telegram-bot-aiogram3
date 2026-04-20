from aiogram import Router, F
from aiogram.types import CallbackQuery
import logging

from app.data.task_manage import get_random_task_from_db, get_task_by_id, get_or_create_ai_solution
from app.data.connection import update_user_task_stat, user_solved_task
from app.keyboards import get_random_task, task_generator, get_help_menu
from app.metrics import REQUESTS_TOTAL, GEMINI_REQUESTS, GEMINI_LATENCY
from app.utils import md_to_telegram_html # Убедись, что ты создал utils.py и перенес туда эту функцию!

router = Router()

@router.callback_query(F.data == "menu_tasks")
async def task_menu(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text("Сгенерируйте случайную задачу: ", reply_markup=get_random_task())


@router.callback_query(F.data.startswith("generate_task_"))
async def generate_task(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    subject = callback.data.replace("generate_task_", "").strip()
    task = await get_random_task_from_db(callback.from_user.id, subject)
    if not task:
        await callback.message.edit_text( "🎉 Ты прорешал ВСЕ задачи по этому предмету в нашей базе! Жди обновлений.", reply_markup=get_help_menu())
        return

    text = (
        f"📝 <b>Задание №{task['task_num']}</b>\n\n"
        f"{task['condition']}\n\n"
        f"<b>Ответ:</b> <tg-spoiler>{task['answer']}</tg-spoiler>"
    )
    await callback.message.edit_text(text, reply_markup=task_generator(task['id']))



@router.callback_query(F.data.startswith("ai_explain_"))
async def ai_explain_handler(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    try:
        task_id = int(callback.data.replace("ai_explain_", "").strip())
    except ValueError:
        await callback.answer("❌ Ошибка: неверный ID задачи", show_alert=True)
        return

    await callback.message.edit_text(
        "🧠 <i>Gemini анализирует задачу и переводит решение на человеческий язык...</i>",
        parse_mode="HTML"
    )

    task = await get_task_by_id(task_id)
    if not task:
        await callback.message.edit_text(
            "❌ Задача не найдена в базе данных.",
            reply_markup=task_generator(task_id)
        )
        return

    try:
        with GEMINI_LATENCY.time():
            raw_answer = await get_or_create_ai_solution(task_id, task['condition'], task['solution'], callback.from_user.id)
            GEMINI_REQUESTS.labels(status='success').inc()

            safe_html_answer = md_to_telegram_html(raw_answer)

            final_text = (
                f"📝 <b>Условие:</b>\n{task['condition']}\n\n"
                f"🧠 <b>AI Объяснение:</b>\n{safe_html_answer}"
            )

            try:
                await callback.message.edit_text(
                    text=final_text[:4090],
                    reply_markup=task_generator(task_id),
                    parse_mode="HTML"
                )

            except Exception as ex:
                logging.warning(f"Сломался HTML парсер: {ex}. Отправляю сырой текст.")

                plain_text = (
                    f"📄 Условие:\n{task['condition']}\n\n"
                    f"🧠 AI Объяснение:\n{raw_answer}"
                )

                await callback.message.edit_text(
                    text=plain_text[:4090],
                    reply_markup=task_generator(task_id),
                    parse_mode=None
                )

    except Exception as e:
        logging.error(f"Ошибка при обращении к Gemini: {e}")
        GEMINI_REQUESTS.labels(status='error').inc()
        fallback_text = (
            f"⚠️ <i>Нейросеть сейчас недоступна. Вывожу стандартное решение из базы:</i>\n\n"
            f"📝 <b>Условие:</b>\n{task['condition']}\n\n"
            f"📖 <b>Официальное решение:</b>\n{task['solution']}\n\n"
            f"🎯 <b>Ответ:</b> {task['answer']}"
        )

        await callback.message.edit_text(
            fallback_text[:4000],
            reply_markup=task_generator(task_id),
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("task_done_"))
async def task_done_handler(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    try:
        task_id = int(callback.data.replace("task_done_", ""))
    except (ValueError, TypeError):
        await callback.answer("❌ Ошибка: неверный ID задачи.", show_alert=True)
        return

    await update_user_task_stat(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        is_correct=True
    )

    await user_solved_task(callback.from_user.id, task_id
            )

    await callback.message.edit_text(
        "✅ <b>Отлично! Задача решена верно.</b>\nГотов к следующей?",
        reply_markup=get_random_task()
    )

@router.callback_query(F.data.startswith("task_failed_"))
async def task_failed_handler(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()

    await update_user_task_stat(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        is_correct=False
    )

    await callback.message.edit_text(
        "❌ <b>Ничего страшного, на ошибках учатся!</b>\nДавай попробуем другую?",
        reply_markup=get_random_task()
    )







