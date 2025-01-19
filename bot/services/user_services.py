from datetime import datetime
from sqlalchemy.exc import IntegrityError
from bot.models.user import User
from sqlalchemy.orm import Session

class UserService:
    def __init__(self, session: Session):
        self.session = session
    def get_chat_id_by_user_id(self, user_id: int) -> int:
        " Получает chat_id переписки с ботом, связанного с пользователем. "
        user = self.session.query(User).filter_by(id=user_id).first()
        return user.chat_id if user else None
    
    def get_user_by_telegram_id(self, telegram_id: int) -> User:
        return self.session.query(User).filter_by(telegram_id=telegram_id).first()
    
    def add_user(self, telegram_id, chat_id, username, first_name, last_name, role):
        try:
            user = self.get_user_by_telegram_id(telegram_id)
            if user:
                # Обновляем chat_id, если пользователь уже существует
                if user.chat_id != chat_id:
                    user.chat_id = chat_id
                    self.session.commit()
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
            return new_user
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Пользователь уже существует.")
