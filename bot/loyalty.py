from .database import SessionLocal
from .models import User

def add_loyalty_points(user_id, points):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if user:
            user.loyalty_points += points
            session.commit()
            return True  # Успешно добавлены баллы
        else:
            return False  # Пользователь не найден
    except Exception as e:
        session.rollback()  # Откат транзакции в случае ошибки
        print(f"Ошибка при добавлении баллов: {e}")
        return False
    finally:
        session.close()  # Закрытие сессии
