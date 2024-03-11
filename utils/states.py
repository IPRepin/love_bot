from aiogram.fsm.state import StatesGroup, State


class MenQuestionnaire(StatesGroup):
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


class WomanQuestionnaire(StatesGroup):
    """
    Модуль определения состояний для машины состояний женских анкет
    """
    PHOTO = State()
    NAME = State()
    AGE = State()
    ABOUT_ME = State()
    FIND = State()
    STATUS = State()