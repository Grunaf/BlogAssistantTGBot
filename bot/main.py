import asyncio
from aiogram import Dispatcher, types
from aiogram.filters.command import Command
from bot.bot_instance import blogger_bot, audience_bot  # Импорт объекта Bot
from flask_app import app  # Импорт Flask-приложения
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL  # Конфигурация
from handlers.audience import handle_audience_start
from handlers.blogger import handle_blogger_start, activate_blogger
from bot.app import app
from database import init_db  # Функция инициализации базы данных

blogger_dp = Dispatcher()
audience_dp = Dispatcher()

# Инициализация базы данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
init_db()  # Создание таблиц в базе данных

# Регистрация обработчиков
audience_dp.message.register(handle_audience_start, Command("start"))
# aud.message.register(handle_message)
blogger_dp.message.register(handle_blogger_start, Command("start"))
blogger_dp.message.register(activate_blogger, Command("activate"))

# Функция запуска Flask
async def run_flask():
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    config = Config()
    config.bind = ["0.0.0.0:5000"]  # Flask будет слушать порт 5000
    await serve(app, config)

# Запуск процесса поллинга новых апдейтов
async def main():
    blogger_task  = blogger_dp.start_polling(blogger_bot)  # Бот работает
    audience_task  = audience_dp.start_polling(audience_bot)  # Бот работает
    flask_task = run_flask()  # Flask работает
    await asyncio.gather(blogger_task, audience_task, flask_task)

if __name__ == "__main__":
    asyncio.run(main())
