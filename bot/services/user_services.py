from datetime import datetime
from sqlalchemy.exc import IntegrityError
from bot.models.user import User
from sqlalchemy.orm import Session
from bot.logger_instance import logger

class UserService:
    def __init__(self, session: Session):
        self.session = session
    def get_chat_id_by_user_id(self, user_id: int) -> int:
        " Получает chat_id переписки с ботом, связанного с пользователем. "
        logger.info(f"Получение chat_id для пользователя с id={user_id}.")
        user = self.session.query(User).filter_by(id=user_id).first()        
        if user:
            logger.info(f"Найден chat_id={user.chat_id} для пользователя с id={user_id}.")
        else:
            logger.warning(f"Пользователь с id={user_id} не найден.")
        return user.chat_id if user else None
    
    def get_user_by_telegram_id(self, telegram_id: int) -> User:        
        """Получает пользователя по его telegram_id."""
        logger.info(f"Получение пользователя с telegram_id={telegram_id}.")
        user = self.session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            logger.info(f"Найден пользователь: id={user.id}, telegram_id={telegram_id}.")
        else:
            logger.warning(f"Пользователь с telegram_id={telegram_id} не найден.")
        return user
    
    def add_user(self, telegram_id, chat_id, username, first_name, last_name, role):
        try:
            logger.info(f"Добавление пользователя с telegram_id={telegram_id}, chat_id={chat_id}.")
            user = self.get_user_by_telegram_id(telegram_id)
            if user:
                # Обновляем chat_id, если пользователь уже существует
                if user.chat_id != chat_id:
                    user.chat_id = chat_id
                    self.session.commit()
                    logger.info(f"Обновлен chat_id пользователя с telegram_id={telegram_id}.")
                else:
                    logger.info(f"Пользователь с telegram_id={telegram_id} уже существует, chat_id не изменен.")
                return user

            # Создание нового пользователя
            new_user = User(
                telegram_id=telegram_id,
                chat_id=chat_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                role=role,
                created_at=datetime.utcnow()
            )
            self.session.add(new_user)
            self.session.commit()
            logger.info(f"Пользователь с telegram_id={telegram_id} успешно добавлен.")
            return new_user
        except IntegrityError as e:
            self.session.rollback()
            logger.error(f"Ошибка добавления пользователя с telegram_id={telegram_id}: {e}")
            raise ValueError("Пользователь уже существует.")
