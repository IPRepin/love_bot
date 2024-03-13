from aiogram.fsm.state import StatesGroup, State


class StatesQuestionnaire(StatesGroup):
    """
    Модуль определения состояний для машины состояний мужских анкет
    """
    PHOTO = State()
    GENDER = State()
    NAME = State()
    AGE = State()
    ABOUT_ME = State()
    FIND = State()
    STATUS = State()
