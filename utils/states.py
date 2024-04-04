from aiogram.fsm.state import StatesGroup, State


class StatesMenQuestionnaire(StatesGroup):
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


class StatesWomanQuestionnaire(StatesGroup):
    """
    Модуль определения состояний для машины состояний женских анкет
    """
    PHOTO = State()
    GENDER = State()
    NAME = State()
    AGE = State()
    ABOUT_ME = State()
    FIND = State()
    STATUS = State()


class UserIdState(StatesGroup):
    USER_ID = State()


class MailingState(StatesGroup):
    CALL_MAILING = State()
    MAIL_TEXT = State()
    ADD_MEDIA = State()
    ADD_BUTTON = State()
    BUTTON_TEXT = State()
    BUTTON_URL = State()
