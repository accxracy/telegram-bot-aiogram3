import re

def build_context_prompt(history_rows, current_prompt):
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