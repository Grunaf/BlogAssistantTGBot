from aiogram import Bot
import os

blogger_bot = Bot(token=os.getenv('API_TOKEN_BLOGGER'))
audience_bot = Bot(token=os.getenv('API_TOKEN_AUDIENCE'))
