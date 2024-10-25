import logging
from typing import Union, List

from celery import Celery
from pusher import Pusher

from app.core import settings

logger = logging.getLogger(__name__)


def make_celery():
    celery = Celery(
        __name__,
        backend=settings.CELERY_RESULT_BACKEND,
        broker=settings.CELERY_BROKER_URL
    )
    return celery


celery = make_celery()

# Khởi tạo Pusher client
pusher_client = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)


@celery.task
def send_notification(channel: Union[int, str], notification_data: dict):
    channel = f'user-{channel}' if isinstance(channel, int) else channel
    try:
        pusher_client.trigger(f'{channel}', f'{notification_data["type"]}', {
            'title': notification_data['title'],
            'content': notification_data['description'],
            'sender': {
                'id': notification_data['sender_id'],
                'name': notification_data['sender_name'],
                'role': notification_data['sender_role']
            }
        })
        logger.info(f"Thông báo được gửi cho người dùng với kênh: {channel}")
    except Exception as e:
        logger.error(f"Lỗi khi gửi thông báo cho người dùng với kênh: {channel}, lỗi: {e}", exc_info=True)


@celery.task
def send_notification_batch(channels: List[Union[int, str]], notification_data: dict):
    batch = []
    for channel in channels:
        batch.append({
            'channel': f'user-{channel}' if isinstance(channel, int) else channel,
            'name': notification_data["type"],
            'data': {
                'title': notification_data['title'],
                'content': notification_data['description'],
                'sender': {
                    'id': notification_data['sender_id'],
                    'name': notification_data['sender_name'],
                    'role': notification_data['sender_role']
                }
            }
        })

    try:
        pusher_client.trigger_batch(batch, False)
        logger.info(f"Thông báo được gửi cho người dùng với kênh: {[item['channel'] for item in batch]}")
    except Exception as e:
        logger.error(f"Lỗi khi gửi thông báo cho người dùng với kênh: {[item['channel'] for item in batch]}, lỗi: {e}", exc_info=True)
