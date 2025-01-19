import logging

# Настройка логгера
logging.basicConfig(
    filename="app.log",  # Файл для логов
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат логов
    datefmt="%Y-%m-%d %H:%M:%S" ,  # Формат времени
)

logger = logging.getLogger(__name__)