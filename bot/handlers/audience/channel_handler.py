from bot.services.blog_metrics_service import BlogMetricsService
from bot.scheduler import schedule_post_metrics
from database import SessionLocal
from bot.bot_instance import blogger_bot
from bot.logger_instance import logger

session = SessionLocal()
blog_service = BlogMetricsService(session, blogger_bot)

def handle_channel_post(data):
    chat_id = data["channel_post"]["chat"]["id"]
    post_id = data["channel_post"]["message_id"]
    user_id = data["channel_post"]["from"]["id"]  # Предполагаем, что поле `from` доступно
    text = data["channel_post"].get("text", "")
    has_image = "photo" in data["channel_post"]
    has_video = "video" in data["channel_post"]

    blog_service.save_post(chat_id, post_id, user_id, text, has_image, has_video)
    schedule_post_metrics(post_id, chat_id)

def handle_my_chat_member(data):
    chat = data["my_chat_member"]["chat"]
    user = data["my_chat_member"]["from"]
    new_status = data["my_chat_member"]["new_chat_member"]["status"]
    logger.info(f"Бот добавлен в канал: {chat['title']} (ID: {chat['id']}) от пользователя {user['username']} (ID: {user['id']})")
    
    if new_status == "administrator":
        blog_service.process_channel_administration(chat, user)