from data.connection import get_connection

async def get_random_task_from_db(telegram_id, subject):
  conn = await get_connection()
  try:
    task = await conn.fetchrow("""
   SELECT id, task_num, condition, solution, answer, photo_id
   FROM ege_tasks
   WHERE subject = $1
   
   -- МАГИЯ ФИЛЬТРАЦИИ ЗДЕСЬ:
   -- Исключаем те ID задач, которые уже связаны с этим пользователем
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
  finally:
    await conn.close()


async def get_task_by_id(task_id):
  conn = await get_connection()
  try:
    task = await conn.fetchrow("SELECT task_num, condition, solution, answer FROM ege_tasks WHERE id = $1", task_id)
    return dict(task) if task else None
  finally:
    await conn.close()
