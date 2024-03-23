from aiogram.types import User, Chat

test_user = User(
    id=1,
    is_bot=True,
    first_name='Test',
    last_name='User',
    username='test_user',
    language_code='ru-RU',
    is_premium=True,
    added_to_attachment_menu=None,
    can_join_groups=None,
    can_read_all_group_messages=None,
    supports_inline_queries=None,
)


test_admin_user = User(
    id=2,
    is_bot=True,
    first_name='Test2',
    last_name='User2',
    username='test_user2',
    language_code='ru-RU',
    is_premium=True,
    added_to_attachment_menu=None,
    can_join_groups=None,
    can_read_all_group_messages=None,
    supports_inline_queries=None,
)


chat = Chat(id=12,
            type='private',
            title='test_chat',
            username=test_user.username,
            first_name=test_user.first_name,
            last_name=test_user.last_name
            )
