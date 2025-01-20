from flask import Flask, request
from bot.logger_instance import logger
from bot.handlers.audience import handle_channel_post, handle_my_chat_member

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    logger.info(f"Получен webhook: {data}")
    if "channel_post" in data:
        handle_channel_post(data)
    elif "my_chat_member" in data:
        handle_my_chat_member(data)
    return "OK", 200
    
@app.route("/")
def home():
    print("home")
    return "Flask работает! Ваш бот тоже!"
