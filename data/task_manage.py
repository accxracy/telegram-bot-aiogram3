
from data import connection
from data.neuro import Neuro


async def get_random_task_from_db(telegram_id, subject):
    async with connection.pool.acquire() as conn:
        task = await conn.fetchrow("""
        SELECT id, task_num, condition, solution, answer
        FROM ege_tasks
        WHERE subject = $1
         AND id NOT IN (
           SELECT ust.task_id 
           FROM user_solved_tasks ust
           JOIN users u ON ust.user_id = u.id
           WHERE u.telegram_id = $2
         )
         ORDER BY RANDOM()
         LIMIT 1
        """, subject, telegram_id)
        return dict(task) if task else None



async def get_task_by_id(task_id):
    async with connection.pool.acquire() as conn:
        task = await conn.fetchrow("SELECT task_num, condition, solution, answer FROM ege_tasks WHERE id = $1", task_id)
        return dict(task) if task else None


async def get_or_create_ai_solution(task_id, task_condition, task_solution, user):
    model = await connection.get_model(user)
    pool = connection.pool


    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT ai_solution FROM ege_tasks WHERE id = $1", task_id)
        if row and row['ai_solution']:
            return row['ai_solution']

    ai = Neuro(model)
    raw_answer = await ai.explain_task(task_condition, task_solution)


    async with pool.acquire() as conn:
        await conn.execute(
        "UPDATE ege_tasks SET ai_solution = $1 WHERE id = $2",
        raw_answer, task_id
        )

    return raw_answer