import logging

# Настройка логгера
logging.basicConfig(
    filename="app.log",  # Файл для логов
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат логов
    datefmt="%Y-%m-%d %H:%M:%S" ,  # Формат времени
)

# Добавление консольного обработчика
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Установите уровень логирования
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.propagate = False