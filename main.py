import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from seed import seed

from metrics import start_metrics_server, REQUESTS_TOTAL, GEMINI_REQUESTS, GEMINI_LATENCY
from config import BOT_TOKEN, ADMIN_ID

from data.neuro import Neuro
from data.math_topics import MATH_TOPICS
from data.topics import TOPICS
from data.materials import MATERIALS
from data.connection import init_db, save_neuro_history, get_user_neuro_history, delete_user_neuro_history,  get_recent_context,     \
check_user_limit, save_user_usage, update_user_task_stat, get_user_stats, user_solved_task, get_user_task_num_stats, get_top_users
from data.task_manage import get_random_task_from_db, get_task_by_id
from io import BytesIO

from keyboards import get_main_menu, get_help_menu, HELP_TEXT, TopicAction, get_topics_menu_physics, \
    get_action_menu_physics, \
    get_topics_menu_mathematics, get_action_menu_mathematics, get_neuro_chat_menu, get_random_task, task_generator, \
    get_list_materials, get_back_to_materials


class NeuroState(StatesGroup):
  waiting_for_prompt = State()

class FeedBack(StatesGroup):
    waiting_for_feedback = State()

class Solve_By_Photo(StatesGroup):
    wait_photo = State()


logging.basicConfig(level=logging.INFO)

bot_token = BOT_TOKEN

if not bot_token:
    raise ValueError("BOT_TOKEN not found in .env")


bot = Bot(token=bot_token,
    default = DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def generate_progress_bar(solved, total):
    if total == 0:
        return "⬜️" * 10 + " 0%"
    percent = (solved / total) * 100
    filled = int((percent / 100) * 10)
    empty = 10 - filled

    return "🟩" * filled + "⬜️" * empty + f" {int(percent)}%"


def md_to_telegram_html(text: str) -> str:
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace('```', '').replace('`', '"')
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<b>\1</b>', text)
    text = re.sub(r'\b_(.*?)_\b', r'<i>\1</i>', text)
    return text



@dp.message(Command("history"))
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

@dp.message(Command("clear_history"))
async def clear_history(message: Message):
    usr = message.from_user.id
    try:
        await delete_user_neuro_history(usr)
        await message.answer("🧹 Твоя история запросов успешно очищена!", reply_markup=get_help_menu())
    except Exception as ex:
        logging.exception(f"Ошибка при удалении истории: {ex}")
        await message.answer("❌ Произошла ошибка. Попробуй позже.")


@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=get_main_menu())

@dp.message(Command("feedback"))
async def feedback_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FeedBack.waiting_for_feedback)
    await message.answer("✅ Напишите ваш отзыв (/cancel для отмены):")

@dp.message(FeedBack.waiting_for_feedback, F.text)
async def feedback(message: Message, state: FSMContext):
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

@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user = message.from_user
    user_link = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

    await message.answer(
        f"👋 Привет, {user_link}! Я бот-помощник по физике и математике!",
        reply_markup=get_main_menu()
    )

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(HELP_TEXT, reply_markup=get_help_menu())

@dp.callback_query(F.data == "menu_help")
async def process_help_menu(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text(
    HELP_TEXT,
    reply_markup=get_help_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "menu_back_to_main")
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

@dp.callback_query(F.data == "menu_physics")
async def process_physics_menu(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text(
  "Выберите раздел физики:",
  reply_markup=get_topics_menu_physics()
    )
    await callback.answer()

@dp.callback_query(F.data == "exit_neuro")
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

@dp.callback_query(F.data == "menu_mathematics")
async def process_mathematics_menu(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text(
    "Выберите раздел математики:",
    reply_markup=get_topics_menu_mathematics()
    )
    await callback.answer()

@dp.callback_query(TopicAction.filter())
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
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            logging.exception(f"Ошибка при обработке callback: {e}")

@dp.callback_query(F.data == "menu_neuro")
async def process_neuro(callback: CallbackQuery, state: FSMContext):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await state.clear()

    await callback.message.edit_text(
        "🤖 Нейро-мод. Модель: gemini-2.5-flash",
        reply_markup=get_help_menu()
    )
    await state.set_state(NeuroState.waiting_for_prompt)


def build_context_prompt(history_rows, current_prompt: str):
    context_parts = [
        "Ты — AI-помощник по математике и физике. "
        "Отвечай понятно, структурно и по делу. "
        "Если новый вопрос связан с предыдущими сообщениями, учитывай контекст. "
        "Если не связан, отвечай только на текущий вопрос.\n"
        "\nВАЖНЫЕ ПРАВИЛА ОФОРМЛЕНИЯ ОТВЕТА:\n"
        "1. Не используй сложную разметку и списки.\n"
        "2. НИКОГДА не вкладывай форматы друг в друга (например, код внутри жирного шрифта или жирный внутри кода).\n"
        "3. Используй жирный шрифт (**) только для заголовков или важных терминов.\n"
        "4. Если нужно написать формулу или кусок кода, просто оберни его в одинарные обратные кавычки `.\n"
    ]

    for row in history_rows:
        row = dict(row)
        context_parts.append(
            f"Пользователь: {row['prompt']}\n"
            f"Ассистент: {row['answer']}\n"
        )

    context_parts.append(f"Пользователь: {current_prompt}\nАссистент:")
    return "\n".join(context_parts)


@dp.message(NeuroState.waiting_for_prompt, F.text)
async def neuro_prompt(message: Message, state: FSMContext):
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
            ai = Neuro()

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

@dp.callback_query(F.data == "menu_tasks")
async def task_menu(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text("Сгенерируйте случайную задачу: ", reply_markup=get_random_task())

@dp.callback_query(F.data.startswith("generate_task_"))
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


@dp.callback_query(F.data.startswith("ai_explain_"))
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
            ai = Neuro()
            raw_answer = await ai.explain_task(task['condition'], task['solution'])
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

            except Exception as e:
                logging.warning(f"Сломался HTML парсер: {e}. Отправляю сырой текст.")

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


@dp.callback_query(F.data == 'menu_profile')
async def show_profile(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    user = callback.from_user

    name = f"@{user.username}" if user.username else user.full_name

    stats = await get_user_stats(user.id)
    task_num_stats = await get_user_task_num_stats(user.id)

    solved = stats['solved']
    unsolved = stats['unsolved']

    total = solved + unsolved
    winrate = int((solved / total) * 100) if total > 0 else 0

    profile_text = (
        f"👤 <b>Твой профиль</b>\n\n"
        f"Пользователь: <b>{name}</b>\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        f"📊 <b>Статистика тренажёра:</b>\n"
        f"✅ Решено верно: <b>{solved}</b>\n"
        f"❌ Ошибок: <b>{unsolved}</b>\n"
        f"🎯 Процент успеха: <b>{winrate}%</b>\n"
    )
    profile_text += f"\n📈 <b>Прогресс по номерам ЕГЭ:</b>\n"
    if not task_num_stats:
        profile_text += "<i>Пока нет решенных задач...</i>"
    else:
        for row in task_num_stats:
            task_num = row['task_num']
            subj_raw = row['subject']
            t_solved = row['solved_count']
            t_total = row['total_in_num']


            translator = {
                'math': 'Математика',
                'physics': 'Физика'
            }

            subj_ru = translator.get(subj_raw, subj_raw)

            bar = generate_progress_bar(t_solved, t_total)
            cup = " 🏆" if t_total > 0 and t_solved == t_total else ""

            profile_text += f"🔹 Задание №{task_num} ({subj_ru}):\n{bar}{cup}\n\n"

    await callback.message.edit_text(
        profile_text,
        reply_markup=get_help_menu()
    )

@dp.callback_query(F.data.startswith("task_done_"))
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

@dp.callback_query(F.data.startswith("task_failed_"))
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


@dp.callback_query(F.data == "menu_useful_materials")
async def useful_materials(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text('Выберите категорию: ', reply_markup=get_list_materials())


@dp.callback_query(F.data.startswith("mat_"))
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
    text = f"<b>{header}</b>\n\n"


    for item in items:
        text += f"🔹 <a href='{item['url']}'>{item['title']}</a>\n"
        text += f"<i>{item['desc']}</i>\n\n"


    await callback.message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=get_back_to_materials()
    )

@dp.callback_query(F.data == "photo_solve")
async def ask_for_photo(callback: CallbackQuery, state: FSMContext):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await callback.message.edit_text(
    "📸 Отправь мне фотографию задачи.\n\n",
    parse_mode="HTML",
    reply_markup=get_help_menu()
    )
    await state.set_state(Solve_By_Photo.wait_photo)


@dp.message(Solve_By_Photo.wait_photo, F.photo)
async def process_photo_task(message: Message, state: FSMContext, bot):
    REQUESTS_TOTAL.labels(type='photo').inc()
    loading_msg = await message.answer("🧠 Анализирую картинку... Это может занять пару секунд. (/cancel для отмены)")
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    downloaded_file = BytesIO()
    await bot.download_file(file.file_path, downloaded_file)
    image_bytes = downloaded_file.getvalue()

    try:
        with GEMINI_LATENCY.time():
            ai_client = Neuro()
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

@dp.message(Solve_By_Photo.wait_photo, F.text)
async def wrong_format_in_photo_state(message: Message, state: FSMContext):
    REQUESTS_TOTAL.labels(type='callback').inc()
    await message.answer("📸 Я жду именно фотографию задачи! \nЕсли передумал, нажми /cancel")

@dp.callback_query(F.data == "leader_board")
async def top(callback: CallbackQuery):
    users = await get_top_users()

    if not users:
        await callback.message.edit_text("Пока что никто не решал задачи. Будь первым! 🥇", reply_markup=get_help_menu())
        return

    text = "🏆 **ТОП ЛИДЕРОВ**\n"
    text += "──────────────────\n\n"

    for i, user in enumerate(users, 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "🔹")

        solved = f"`{user['solved']:<3}`"
        username = user['username']

        text += f"{medal} @{username:<12} | {solved} задач\n"

    text += "\n──────────────────"

    text += "\n🔄 *Обновляется в реальном времени*"

    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_help_menu())


async def main():
    start_metrics_server(port=8000)
    await init_db()
    await seed()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

