from aiogram import types
from bot.database import SessionLocal
from bot.models.user import UserRole
from bot.services.user_services import UserService

async def handle_blogger_start(message: types.Message):
    user_service = UserService(SessionLocal())
    user = user_service.add_user(
        telegram_id=message.from_user.id,
        chat_id=message.chat.id, 
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        role=UserRole.Blogger
    )

    if user.is_confirmed:
        await message.reply("Добро пожаловать, блогер! Вы подтвержденный клиент.")
    else:
        await message.reply(
            "Добро пожаловать, блогер! Ваш аккаунт пока не подтвержден. "
            "Отправьте ключ активации в следующем формате: /activate [ключ доступа]"
            "Без квадратных скобок"
            "Если вы не приобретали тариф, можете ознакомиться с продуктом по следующей ссылке"
        )