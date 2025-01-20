import requests
from bot.models.user import Channel
from bot.models.post import Post, PostMetric
from bot.services.user_services import UserService 
from datetime import datetime
from bot.logger_instance import logger
from config import API_TOKEN_METRIC

TELEGRAM_API_URL = f"https://api.telegram.org/bot{API_TOKEN_METRIC}"

class BlogMetricsService:
    def __init__(self, session, bot):
        self.session = session
        self.bot = bot  # Экземпляр Telegram бота
        self.user_service = UserService(session)  # Создаем экземпляр UserService

    async def send_message_to_user(self, chat_id, user_id, message):
        """Отправка сообщения пользователю."""
        try:
            self.bot.send_message(chat_id=chat_id, text=message)
            logger.info(f"Сообщение успешно отправлено пользователю {user_id}.")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

    def save_post(self, chat_id, post_id, user_id, text, has_image=False, has_video=False):
        try:
            post = Post(
                channel_id=chat_id,
                message_id=post_id,
                user_id=user_id,
                text=text,
                has_image=has_image,
                has_video=has_video,
                published_at=datetime.utcnow()
            )
            self.session.add(post)
            self.session.commit()
            logger.info(f"Пост {post_id} в канале {chat_id} успешно сохранён.")
        except Exception as e:
            logger.error(f"Ошибка при сохранении поста: {e}")

    def collect_post_metrics(self, post_id, channel_id):
        url = f"{TELEGRAM_API_URL}/getChat"
        response = requests.get(url, params={"chat_id": channel_id})
        if response.status_code == 200:
            metrics = response.json()
            views = metrics.get("view_count", 0)
            likes = metrics.get("like_count", 0)
            # Save metrics to the database
            post_metric = PostMetric(post_id=post_id, views=views, likes=likes, collected_at=datetime.utcnow())
            self.session.add(post_metric)
            self.session.commit()

    def process_channel_administration(self, chat, user):
        """Обработка добавления бота в канал."""
        try:

            with self.session as session:
                existing_user = self.user_service.get_user_by_telegram_id(user["id"])
                if existing_user:
                    channel = Channel(
                        telegram_id=chat["id"],
                        title=chat.get("title"),
                        username=chat.get("username"),
                        user_id=existing_user.id,
                        added_at=datetime.utcnow()
                    )
                    session.add(channel)
                    session.commit()
                    message_success_added_to_channel = f"Канал {chat['title']} успешно привязан к пользователю {existing_user.username}."
                    logger.info(message_success_added_to_channel)
                    self.send_message_to_user(chat["id"], existing_user.id, message_success_added_to_channel)
                else:
                    logger.warning(f"Бот добавлен сторонним пользователем. ID канала: {chat['id']}.")
                    self.leave_channel(chat["id"])
        except Exception as e:
            logger.error(f"Ошибка при обработке администрирования канала: {e}")

    def leave_channel(self, chat_id):
        """Удаление бота из канала."""
        url = f"{TELEGRAM_API_URL}/leaveChat"
        response = requests.post(url, json={"chat_id": chat_id})
        if response.status_code == 200:
            logger.info(f"Бот успешно покинул канал {chat_id}.")
        else:
            logger.error(f"Ошибка при удалении бота из канала {chat_id}: {response.text}")
