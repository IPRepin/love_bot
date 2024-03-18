import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires

logger = logging.getLogger(__name__)
db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()
main_admin_router = Router()


@main_admin_router.callback_query(F.data.in_(['approved', 'rejected']))
async def approve(query: types.CallbackQuery,
                  state: FSMContext) -> None:
    if query.data == 'approved':
        await query.message.answer("You have been approved")
    elif query.data == 'rejected':
        await query.message.answer("You have been rejected")