from datetime import datetime, timedelta
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from sqlalchemy import func, cast, String
from sqlalchemy.orm import Session
from bot.database import SessionLocal
from bot.models import UserRole, Document, Test
from bot.bot_instance import blogger_bot
from bot.services.user_services import UserService

async def handle_audience_start(message: types.Message):
    session = SessionLocal()

    user_service = UserService(session)
    user_service.add_user(
        telegram_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        role=UserRole.Audience
    )
    await message.reply("Добро пожаловать! Наслаждайтесь нашими тестами и материалами.")

    # # Получаем список документов из базы данных
    # documents = session.query(Document).all()

    # if documents:
    #     # Создаем клавиатуру с чек-листами
    #     keyboard = InlineKeyboardMarkup(row_width=1)
    #     for document in documents:
    #         keyboard.add(
    #             InlineKeyboardButton(document.title, callback_data=f"checklist_{document.id}")
    #         )

    #     # Приветственное сообщение с предложением выбрать чек-лист
    #     await bot.send_message(
    #         message.from_user.id,
    #         "📋 Привет! Выберите один из чек-листов, который вас интересует:",
    #         reply_markup=keyboard,
    #     )
    # else:
    #     # Если чек-листы недоступны, предлагаем популярный тест
    #     keyboard = InlineKeyboardMarkup(row_width=1)

    #     # Проверяем популярные тесты в базе данных
    #     popular_test = get_popular_test_id(session)

    #     if popular_test:
    #         # Предлагаем самый популярный тест
    #         keyboard.add(
    #             InlineKeyboardButton(f"Пройти тест: {popular_test.title}", callback_data=f"test_{popular_test.id}")
    #         )
    #     else:
    #         test = session.query(Test).order_by(func.random()).first()  # Случайный тест
    #         if test:
    #             # Если нет данных о популярности, предлагаем общий тест
    #             keyboard.add(
    #                 InlineKeyboardButton(f"Пройти тест: {test.title}", callback_data=f"test_{test.id}")
    #             )

    #     # Добавляем кнопку для ознакомления с кастомными ботами
    #     keyboard.add(
    #         InlineKeyboardButton("Узнать о кастомных ботах", callback_data="learn_bots")
    #     )

    #     await bot.send_message(
    #         message.from_user.id,
    #         "К сожалению, чек-листы пока недоступны. Но вы можете:",
    #         reply_markup=keyboard,
    #     )
    # session.close()

# Функция для определения самого популярного теста

# def get_popular_test_id(session: Session, time_frame: timedelta = timedelta(days=30), min_data_count=10):
#     # Получаем текущую дату
#     now = datetime.utcnow()

#     # Фильтруем действия "CompletedTest" и извлекаем данные
#     query = session.query(
#         cast(ActivityLog.details["test_id"], String).label("test_id"),
#         func.count(ActivityLog.id).label("count")
#     ).filter(
#         ActivityLog.action == "Action.CompletedTest"
#     )

#     # Проверяем, если есть данные за указанный период (например, 30 дней)
#     if time_frame:
#         start_date = now - time_frame
#         query = query.filter(ActivityLog.timestamp >= start_date)

#     # Получаем общее количество записей за этот период
#     total_records = query.count()

#     # Если данных меньше чем min_data_count, возвращаем None
#     if total_records < min_data_count:
#         return None
    
#     # Группируем по test_id и сортируем по популярности
#     query = query.group_by("test_id").order_by(func.count(ActivityLog.id).desc())

#     # Возвращаем самый популярный test_id
#     result = query.first()  # Используем first(), чтобы получить только один тест
#     if result:
#         return int(result.test_id)
#     return None

#     # # Создаем inline-клавиатуру
#     # keyboard = InlineKeyboardMarkup(row_width=1)
#     # keyboard.add(
#     #     InlineKeyboardButton("Пройти викторину", callback_data="start_test"),
#     #     InlineKeyboardButton("Посмотреть чек-листы", callback_data="view_checklists"),
#     #     InlineKeyboardButton("Узнать о кастомных ботах", callback_data="learn_bots")
#     # )

#     # # Отправляем приветственное сообщение
#     # await message.answer(
#     #     f"Привет, {message.from_user.first_name}! Добро пожаловать в помощника ботов! 🚀\n\n"
#     #     "Здесь вы узнаете, как кастомный бот может автоматизировать процессы, "
#     #     "повысить вовлеченность и помочь вам зарабатывать больше.\n\n"
#     #     "Готовы начать? Давайте с быстрого теста, чтобы понять вашу текущую ситуацию!",
#     #     reply_markup=keyboard
#     # )

#     # Закрытие сессии
