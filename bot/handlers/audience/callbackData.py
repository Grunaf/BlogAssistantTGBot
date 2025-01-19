from aiogram import types
from bot.database import SessionLocal
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from sqlalchemy import func
from bot.models import Document, Test
from bot.bot_instance import bot
from start import get_popular_test_id

# Функция для обработки callback_query
async def send_checklist(callback_query: types.CallbackQuery):
    session = SessionLocal()

    if callback_query.data.startswith("checklist_"):
        # Извлекаем ID выбранного документа из callback_data
        document_id = int(callback_query.data.split("_")[1])
        document = session.query(Document).filter(Document.id == document_id).first()

        if document:
            try:
                # Отправляем выбранный файл пользователю
                await bot.answer_callback_query(callback_query.id)
                await bot.send_message(
                    callback_query.from_user.id, f"Вот ваш чек-лист: {document.title}"
                )
                await bot.send_document(callback_query.from_user.id, InputFile(document.file_path))

# через время отправить уведомление о том как он понял чек лист, помогла ли информация. Тест
# дать ему 
            except Exception as e:
                await bot.send_message(
                    callback_query.from_user.id,
                    f"Произошла ошибка при отправке документа: {e}",
                )
        else:
            # Если чек-лист не найден, показываем популярный тест или случайный тест
            popular_test_id = get_popular_test_id(session)

            keyboard = InlineKeyboardMarkup(row_width=1)

            if popular_test_id:
                # Если есть популярный тест, предлагаем его
                popular_test = session.query(Test).get(popular_test_id)
                if popular_test:
                    keyboard.add(
                        InlineKeyboardButton(f"Пройти тест: {popular_test.title}", callback_data=f"test_{popular_test.id}")
                    )
            else:
                # Если нет данных о популярности, выбираем случайный тест
                test = session.query(Test).order_by(func.random()).first()
                if test:
                    keyboard.add(
                        InlineKeyboardButton(f"Пройти тест: {test.title}", callback_data=f"test_{test.id}")
                    )

            # Добавляем кнопку для ознакомления с кастомными ботами
            keyboard.add(
                InlineKeyboardButton("Узнать о кастомных ботах", callback_data="learn_bots")
            )

            # Отправляем сообщение с предложением пройти тест
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                callback_query.from_user.id,
                "К сожалению, чек-лист не найден. Но вы можете пройти популярный тест или узнать о кастомных ботах:",
                reply_markup=keyboard,
            )

        session.close()
