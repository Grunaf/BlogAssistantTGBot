from apscheduler.schedulers.background import BackgroundScheduler
from bot.services.blog_metrics_service import BlogMetricsService
from bot.logger_instance import logger
from database import SessionLocal
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()
session = SessionLocal()

def fetch_metrics_task(post_id, channel_id):
    """Задача для сбора метрик поста."""
    try:
        blog_service = BlogMetricsService(session)
        blog_service.collect_post_metrics(post_id, channel_id)
        logger.info(f"Метрики для поста {post_id} в канале {channel_id} успешно собраны.")
    except Exception as e:
        logger.error(f"Ошибка при сборе метрик для поста {post_id} в канале {channel_id}: {e}")

def schedule_post_metrics(post_id, channel_id, intervals=[24]):
    """
    Планирует задачи для сбора метрик через указанные интервалы времени.
    
    Args:
        post_id (int): ID поста.
        channel_id (int): ID канала.
        intervals (list): Список интервалов в часах.
    """
    for interval in intervals:
        run_date = datetime.utcnow() + timedelta(hours=interval)
        scheduler.add_job(
            fetch_metrics_task,
            'date',
            run_date=run_date,
            args=[post_id, channel_id]
        )
        logger.info(f"Сбор метрик для поста {post_id} в канале {channel_id} запланирован через {interval} часов.")

# Запуск планировщика
scheduler.start()
