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
        # Tạo tên kênh cho người dùng
        user_channel = f'{channel}' if isinstance(channel, int) else channel

        # Tạo thông tin dữ liệu thông báo từ notification_data
        notification_content = {
            'title': notification_data.get('title', 'Thông báo'),
            'description': notification_data.get('description', ''),
            'doctor': {
                'name': notification_data.get('doctor_name', ''),
                'clinic_location': notification_data.get('clinic_location', '')
            },
            'start_date':notification_data.get('start_date', ''),
            'start_time':notification_data.get('start_time', ''),
        }

        # Thêm vào batch để gửi thông báo
        batch.append({
            'channel': user_channel,
            'name': "notification",
            'data': notification_content
        })

    try:
        # Gửi thông báo theo dạng batch qua `pusher_client`
        pusher_client.trigger_batch(batch, False)
        logger.info(f"Thông báo đã được gửi cho người dùng qua các kênh: {[item['channel'] for item in batch]}")
    except Exception as e:
        # Log chi tiết nếu có lỗi
        logger.error(
            f"Lỗi khi gửi thông báo cho các kênh: {[item['channel'] for item in batch]}, lỗi: {str(e)}",
            exc_info=True
        )
