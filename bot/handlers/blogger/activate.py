from aiogram import types
from bot.database import SessionLocal
from bot.models import UserRole, AccessKey
from bot.services.user_services import UserService
from bot.logger_instance import logger

async def activate_blogger(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.reply("Используйте команду в формате: /activate <ключ>")
        logger.warning(f"Пользователь {message.from_user.id} ввел неверный формат команды: {message.text}")
        return

    access_key = args[1]
    session = SessionLocal()

    try:
        # Проверка ключа
        key = session.query(AccessKey).filter_by(key=access_key, is_active=True).first()
        if not key:
            await message.reply("Ключ недействителен или уже использован.")
            logger.warning(f"Ключ {access_key} недействителен или уже использован пользователем {message.from_user.id}.")
            return

        # Проверка пользователя
        user_service = UserService(session)
        user = user_service.get_user_by_telegram_id(message.from_user.id)

        if not user:
            await message.reply("Сначала используйте /start для регистрации.")
            logger.warning(f"Пользователь {message.from_user.id} не найден. Команда /activate отклонена.")
            return

        if user.role == UserRole.Blogger and user.is_confirmed_blogger:
            logger.info(f"Пользователь {message.from_user.id} уже активирован как блогер.")
            await message.reply("Вы уже активированы как блогер.")
            return

        # Активация роли и тарифа
        user.is_confirmed_blogger = True
        user.tariff = key.tariff  # Присваиваем тариф из ключа
        key.is_active = False  # Деактивируем ключ
        session.commit()

        logger.info(
            f"Пользователь {message.from_user.id} успешно активирован как блогер с тарифом {key.tariff}."
        )
        await message.reply(f"Вы успешно активированы как блогер! Вам присвоен тариф: {key.tariff}.")
    except Exception as e:
        logger.error(f"Ошибка при активации пользователя {message.from_user.id}: {e}")
        await message.reply("Произошла ошибка. Попробуйте позже.")
    finally:
        session.close()