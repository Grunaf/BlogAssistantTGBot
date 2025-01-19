from aiogram import types
from bot.database import SessionLocal
from bot.models import UserRole, AccessKey
from bot.services.user_services import UserService

async def activate_blogger(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.reply("Используйте команду в формате: /activate <ключ>")
        return

    access_key = args[1]
    session = SessionLocal()

    # Проверка ключа
    key = session.query(AccessKey).filter_by(key=access_key, is_active=True).first()
    if not key:
        await message.reply("Ключ недействителен или уже использован.")
        return

    # Проверка пользователя
    user_service = UserService(session)
    user = user_service.get_user_by_telegram_id(message.from_user.id)

    if not user:
        await message.reply("Сначала используйте /start для регистрации.")
        return

    if user.role == UserRole.Blogger:
        await message.reply("Вы уже активированы как блогер.")
        return

    # Активация роли и тарифа
    user.is_confirmed_blogger = True
    user.tariff = key.tariff  # Присваиваем тариф из ключа
    key.is_active = False  # Деактивируем ключ
    session.commit()

    await message.reply(f"Вы успешно активированы как блогер! Вам присвоен тариф: {key.tariff}.")