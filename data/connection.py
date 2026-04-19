import asyncpg
import logging


from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


async def get_connection():
    return await asyncpg.connect(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        host=DB_HOST,
        port=int(DB_PORT)
    )


async def init_db():
    conn = await get_connection()
    try:
        with open("01_init.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()


        await conn.execute(sql_script)
        logging.info("✅ База данных успешно инициализирована из 01_init.sql")

    except Exception as e:
        logging.error(f"❌ Ошибка при создании таблиц: {e}")

    await conn.close()


async def save_neuro_history(telegram_id, username, prompt, answer, model):
    conn = await get_connection()

    await conn.execute("""
        INSERT INTO neuro_history (telegram_id, username, prompt, answer, model)
        VALUES ($1, $2, $3, $4, $5)
    """, telegram_id, username, prompt, answer, model)

    await conn.close()


async def get_user_neuro_history(telegram_id):
    conn = await get_connection()
    rows = await conn.fetch("""
        SELECT *
        FROM neuro_history
        WHERE telegram_id = $1
        ORDER BY created_at DESC
        LIMIT 10
    """, telegram_id)
    await conn.close()
    return rows


async def delete_user_neuro_history(telegram_id):
    conn = await get_connection()
    await conn.execute("""
        DELETE  FROM neuro_history
        WHERE telegram_id = $1

    """, telegram_id)
    await conn.close()


async def get_recent_context(telegram_id, limit=3):
    conn = await get_connection()
    rows = await conn.fetch("""
        SELECT prompt, answer
        FROM neuro_history
        WHERE telegram_id = $1
        ORDER BY created_at DESC
        LIMIT $2
    """, telegram_id, limit)
    await conn.close()

    return list(reversed(rows))


async def check_user_limit(telegram_id, limit=20):
    conn = await get_connection()

    count = await conn.fetchval("""
    SELECT COUNT(*)
    FROM neuro_usage
    WHERE telegram_id = $1 AND DATE(created_at) = CURRENT_DATE
  """, telegram_id)

    await conn.close()

    return count < limit


async def save_user_usage(telegram_id):
    conn = await get_connection()

    await conn.execute("""
        INSERT INTO neuro_usage (telegram_id)
        VALUES ($1)
    """, telegram_id)

    await conn.close()


async def update_user_task_stat(telegram_id, username, is_correct):
    conn = await get_connection()
    try:
        if is_correct:
            await conn.execute("""
    INSERT INTO users (telegram_id, username, solved, unsolved)
    VALUES ($1, $2, 1, 0)
    ON CONFLICT (telegram_id) 
    DO UPDATE SET 
     solved = users.solved + 1,
     username = EXCLUDED.username;
   """, telegram_id, username)
        else:
            await conn.execute("""
    INSERT INTO users (telegram_id, username, solved, unsolved)
    VALUES ($1, $2, 0, 1)
    ON CONFLICT (telegram_id) 
    DO UPDATE SET 
     unsolved = users.unsolved + 1,
     username = EXCLUDED.username;
   """, telegram_id, username)
    finally:
        await conn.close()


async def get_user_stats(telegram_id):
    conn = await get_connection()
    try:
        user = await conn.fetchrow("""
        SELECT solved, unsolved 
        FROM users 
        WHERE telegram_id = $1
        """, telegram_id)

        if user:
            return dict(user)
        return {"solved": 0, "unsolved": 0}
    finally:
        await conn.close()


async def user_solved_task(telegram_id, task_id):
    conn = await get_connection()
    try:
        await conn.execute("""
              INSERT INTO user_solved_tasks (user_id, task_id)
              VALUES (
                (SELECT id FROM users WHERE telegram_id = $1), 
                $2
              )
              ON CONFLICT (user_id, task_id) DO NOTHING;
            """, telegram_id, task_id)
    finally:
        await conn.close()


async def get_user_task_num_stats(telegram_id):
    conn = await get_connection()
    try:
        user_record = await conn.fetchrow("SELECT id FROM users WHERE telegram_id = $1", telegram_id)

        if not user_record:
            return []

        user_id = user_record['id']

        total_records = await conn.fetch("""
      SELECT subject, task_num, COUNT(id) as total_count 
      FROM ege_tasks 
      GROUP BY subject, task_num;
    """)

        total_dict = {(row['subject'], row['task_num']): row['total_count'] for row in total_records}

        solved_records = await conn.fetch("""
   SELECT ege_tasks.subject, ege_tasks.task_num, COUNT(user_solved_tasks.task_id) as solved_count
   FROM user_solved_tasks
   INNER JOIN ege_tasks ON user_solved_tasks.task_id = ege_tasks.id
   WHERE user_solved_tasks.user_id = $1
   GROUP BY ege_tasks.subject, ege_tasks.task_num
   ORDER BY ege_tasks.subject, ege_tasks.task_num;
  """, user_id)

        result = []
        for row in solved_records:
            subj = row['subject']
            t_num = row['task_num']
            s_count = row['solved_count']

            t_total = total_dict.get((subj, t_num), 0)

            result.append({
                'subject': subj,
                'task_num': t_num,
                'solved_count': s_count,
                'total_in_num': t_total
            })

        return result

    except Exception as ex:
        logging.error(f"Ошибка: {ex}")
        return []
    finally:
        await conn.close()

async def get_top_users():
    conn = await get_connection()
    rows = await conn.fetch("SELECT username, solved FROM users ORDER BY solved DESC LIMIT 10")
    return rows
