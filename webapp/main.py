from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
import logging
from app.data.task_manage import get_random_task_from_db, get_task_by_id, get_or_create_ai_solution
from app.data import connection
from app.metrics import DB_QUERY_TIME, TASK_GENERATED, REQUEST_ERRORS
from prometheus_fastapi_instrumentator import Instrumentator
logging.basicConfig(level=logging.INFO)


class AnswerCheck(BaseModel):
    tg_id: int
    task_id: int
    user_answer: str
    username: str


@asynccontextmanager
async def lifespan(app):
    print("Подключение к БД")
    await connection.init_pool()

    yield

    print("Отключение от БД")
    if connection.pool:
        await connection.pool.close()


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="webapp/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/api/get_task")
async def get_task(tg_id: int, subject):
    with DB_QUERY_TIME.time():
        task = await get_random_task_from_db(tg_id, subject)
        TASK_GENERATED.inc()
        if not task:
            REQUEST_ERRORS.inc()
            return {"success": False, "error": f"Задачи по {subject} закончились!"}

        return {
            "success": True,
            "task_id": task['id'],
            "task_number": task['task_num'],
            "task_text": task['condition']
        }


@app.post("/api/check_answer")
async def check_answer(data: AnswerCheck):
    with DB_QUERY_TIME.time():
        task = await get_task_by_id(data.task_id)


    if not task:
        logging.warning(f"Task check attempted for non-existent id: {data.task_id}")
        REQUEST_ERRORS.inc()
        return {"success": False, "error": "Задача не найдена"}



    correct_answer = str(task['answer']).strip().lower()
    user_answer_clean = data.user_answer.strip().lower()

    is_correct = (correct_answer == user_answer_clean)

    with DB_QUERY_TIME.time():
        await connection.update_user_task_stat(data.tg_id, data.username, is_correct)

        if is_correct:
            await connection.user_solved_task(data.tg_id, data.task_id)


    return {
        "success": True,
        "is_correct": is_correct,
        "correct_answer": task['answer'],
        "solution": task.get('solution', 'Решения пока нет :(')
    }


@app.get("/api/get_ai_explanation")
async def get_ai_explanation(tg_id: int, task_id: int):
    with DB_QUERY_TIME.time():
        task = await get_task_by_id(task_id)
        if not task:
            return {"success": False, "error": "Задача не найдена"}

        try:
            explanation = await get_or_create_ai_solution(
                task_id, task['condition'], task['solution'], tg_id
            )
            return {"success": True, "explanation": explanation}

        except Exception as ex:
            logging.error(f"Neuro: {ex}")

            fallback_text = (
                f"⚠️Нейросеть сейчас недоступна. Вывожу стандартное решение из базы:\n\n"
                f"📝 Условие:\n{task['condition']}\n\n"
                f"📖 Официальное решение:\n{task['solution']}\n\n"
                f"🎯 Ответ: {task['answer']}"
            )


            return {"success": True, "explanation": fallback_text}


Instrumentator().instrument(app).expose(app)