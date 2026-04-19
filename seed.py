import json
import os
import logging
import data.connection

async def seed():
    file_path = os.path.join(os.path.dirname(__file__), 'data/tasks.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        async with data.connection.pool.acquire() as conn:
            async with conn.transaction():
                for t in tasks:
                    await conn.execute("""
                INSERT INTO ege_tasks (subject, task_num, condition, solution, answer)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (subject, condition) DO UPDATE SET
                solution = EXCLUDED.solution,
                answer = EXCLUDED.answer;
              """, t['subject'], t['task_num'], t['condition'], t['solution'], t['answer'])

        logging.info("✅ База данных успешно заполнена")
    except Exception as ex:
        logging.error(f"❌ Ошибка: {ex}")
