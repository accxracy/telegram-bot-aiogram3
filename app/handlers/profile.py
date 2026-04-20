from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.data.connection import get_model, get_user_stats, get_user_task_num_stats, get_top_users
from app.keyboards import get_help_menu
from app.metrics import REQUESTS_TOTAL
from app.utils import generate_progress_bar

router = Router()

@router.callback_query(F.data == 'menu_profile')
async def show_profile(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
    user = callback.from_user

    model = await get_model(callback.from_user.id)

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
        profile_text += "<i>Пока нет решенных задач...</i>\n\n"
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

    profile_text += f"⚙️ <b>Текущая модель:</b> <code>{model}</code>"

    await callback.message.edit_text(
        profile_text,
        reply_markup=get_help_menu()
    )

@router.callback_query(F.data == "leader_board")
async def top(callback: CallbackQuery):
    REQUESTS_TOTAL.labels(type='callback').inc()
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