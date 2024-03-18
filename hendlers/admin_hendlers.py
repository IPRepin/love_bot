import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from utils.states import UserIdState

logger = logging.getLogger(__name__)
db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()
main_admin_router = Router()


# TODO Создать функцию, которая изменяет статус модерации в БД
@main_admin_router.callback_query(F.data.in_(['approved', 'rejected']), UserIdState.USER_ID)
async def moderation_questionnaires(query: types.CallbackQuery,
                  state: FSMContext) -> None:
    logger.info(query.data)
    data = await state.get_data()
    await state.clear()
    user_id = data.get('user_id')
    logger.info(f'user_id: {user_id}')
    if query.data == 'approved' and db_men.profile_exists(user_id=user_id) \
            or db_woman.profile_exists(user_id=user_id):
        await query.message.answer("✅Анкета одобрена")
        await query.answer()
    elif query.data == 'rejected' and db_men.profile_exists(user_id=user_id) \
            or db_woman.profile_exists(user_id=user_id):
        await query.message.answer("🚫Анкета отклонена")
        await query.answer()
