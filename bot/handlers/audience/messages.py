from aiogram import types
from bot.database import SessionLocal
from bot.models import User

async def handle_message(message: types.Message):
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        await message.reply("Пожалуйста, начните с команды /start.")
        return

    # user.interest = message.text
    # session.commit()
    # await message.reply(f"Ваш интерес: {message.text} сохранен!")
