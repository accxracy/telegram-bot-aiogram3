import json
import os
import logging
from data.connection import get_connection

async def seed():
    conn = None
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'data/tasks.json')

        conn = await get_connection()
        with open(file_path, 'r', encoding='utf-8') as f:
            tasks = json.load(f)

        for t in tasks:
            await conn.execute("""
            INSERT INTO ege_tasks (subject, task_num, condition, solution, answer)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (subject, condition) DO UPDATE SET
              solution = EXCLUDED.solution,
              answer = EXCLUDED.answer;
          """, t['subject'], t['task_num'], t['condition'], t['solution'], t['answer'])
        await conn.close()
        logging.info("✅seed.py")
    except Exception as ex:
        logging.error(f"❌seed.py {ex}")
    finally:
        if conn:
            await conn.close()
