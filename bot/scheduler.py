from apscheduler.schedulers.background import BackgroundScheduler
from bot.services.blog_metrics_service import BlogMetricsService
from bot.logger_instance import logger
from database import SessionLocal

scheduler = BackgroundScheduler()
session = SessionLocal()

def fetch_metrics_task(post_id, channel_id):
    blog_service = BlogMetricsService(session)
    blog_service.collect_post_metrics(post_id, channel_id)

def schedule_post_metrics(post_id, channel_id):
    # from datetime import datetime, timedelta
    # run_date = datetime.utcnow() + timedelta(hours=24)
    # scheduler.add_job(fetch_metrics_task, 'date', run_date=run_date, args=[post_id, channel_id])
    
    # Заглушка для планирования метрик
    logger.info(f"Планирование сбора метрик для поста {post_id} в канале {channel_id}")

scheduler.start()
