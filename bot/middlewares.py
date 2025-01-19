from aiogram import types
from aiogram import BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Логируем информацию о сообщении
        print(f"Получено сообщение от {message.from_user.username}: {message.text}")

    async def on_post_process_message(self, message: types.Message, data: dict, result: any):
        # Логируем результат обработки сообщения
        print(f"Обработка сообщения завершена: {result}")
