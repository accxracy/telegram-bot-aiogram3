from aiogram.fsm.state import State, StatesGroup

class NeuroState(StatesGroup):
  waiting_for_prompt = State()

class FeedBack(StatesGroup):
    waiting_for_feedback = State()

class Solve_By_Photo(StatesGroup):
    wait_photo = State()
