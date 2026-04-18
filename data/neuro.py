import logging
from google import genai
from google.genai import types

from config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

class Neuro:
    def __init__(self, model_name = "gemini-2.5-flash"):
        self.model_name = model_name

    async def make_response(self, prompt):
        try:
            response = await client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt
             )
            return response.text
        except Exception as ex:
            logging.error(f"Ошибка нового Gemini API: {ex}")
            raise ex

    async def solve_from_photo(self, image_bytes):
     prompt = (
      "Ты — строгий, но справедливый репетитор по математике ЕГЭ. "
      "Прочитай условие задачи с прикрепленной фотографии и напиши подробное, пошаговое решение.\n\n"
      "ВАЖНЫЕ ПРАВИЛА ОФОРМЛЕНИЯ ОТВЕТА:\n"
      "1. Не используй сложную разметку и списки.\n"
      "2. НИКОГДА не вкладывай форматы друг в друга (например, код внутри жирного шрифта).\n"
      "3. Используй жирный шрифт (**) только для заголовков.\n"
      "4. Если нужно написать формулу или кусок кода, просто оберни его в одинарные обратные кавычки `.\n"
      "5. Если на фото вообще нет задачи по математике, ответь коротко: 'На фото не видно математической задачи'."
     )

     try:
      image_part = types.Part.from_bytes(
       data=image_bytes,
       mime_type='image/jpeg'
      )
      response = await client.aio.models.generate_content(
       model=self.model_name,
       contents=[image_part, prompt]
      )
      return response.text

     except Exception as ex:
      logging.error(f"Ошибка Gemini API при чтении фото: {ex}")
      raise ex



    async def explain_task(self, condition, solution):
        prompt = (
         "Ты — строгий, но справедливый репетитор по подготовке к ЕГЭ. "
         "Твоя задача — максимально понятно и пошагово объяснить ученику решение задачи.\n\n"
         f"📝 УСЛОВИЕ:\n{condition}\n\n"
         f"📖 ОФИЦИАЛЬНОЕ РЕШЕНИЕ:\n{solution}\n\n"
         "Выдай структурированное объяснение с использованием списков и выделений. "
         "Опирайся только на предоставленное решение."
         "\nВАЖНЫЕ ПРАВИЛА ОФОРМЛЕНИЯ ОТВЕТА:\n"
         "1. Не используй сложную разметку и списки.\n"
         "2. НИКОГДА не вкладывай форматы друг в друга (например, код внутри жирного шрифта или жирный внутри кода).\n"
         "3. Используй жирный шрифт (**) только для заголовков или важных терминов.\n"
         "4. Если нужно написать формулу или кусок кода, просто оберни его в одинарные обратные кавычки `.\n"
              )
        return await self.make_response(prompt)
