import logging

from bson import ObjectId, errors
from pymongo import UpdateOne
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant import COLLECTION_NAME, AppStatus
from app.core import error_exception_handler
from app.database import db
from app.utils import convert_to_DMY_str

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_notification(self, user_id: int):
        collection = db[COLLECTION_NAME]
        notifications_cursor = collection.find(
            {"to_notify_users": {"$in": [user_id]}},
            {
                "_id": 1,
                "title": 1,
                "description": 1,
                "sender_id": 1,
                "sender_name": 1,
                "sender_role": 1,
                "created_at": 1,
                "seen_users": 1,
                "doctor_name": 1,
                "clinic_location": 1,
                "start_date": 1,
                "start_time": 1
            }
        ).sort("created_at", -1)

        notifications = []
        for notification in notifications_cursor:
            # Convert ObjectId to string for JSON serialization
            notification['_id'] = str(notification['_id'])

            # Convert created_at to dd/mm/yyyy format
            created_at = notification.get("created_at")
            if created_at:
                notification["created_at"] = convert_to_DMY_str(created_at)
            if user_id in notification.get("seen_users", []):
                notification["is_seen"] = True
            else:
                notification["is_seen"] = False
            del notification["seen_users"]
            notifications.append(notification)

        return notifications

    async def get_notification_unseen(self, user_id: int):
        collection = db[COLLECTION_NAME]
        notifications_cursor = collection.find(
            {"to_notify_users": {"$in": [user_id]}},
            {
                "_id": 1,
                "title": 1,
                "description": 1,
                "sender_id": 1,
                "sender_name": 1,
                "sender_role": 1,
                "created_at": 1,
                "seen_users": 1,
                "doctor_name": 1,
                "clinic_location": 1,
                "start_date": 1,
                "start_time": 1
            }
        ).sort("created_at", -1)

        notifications = []
        for notification in notifications_cursor:
            # Convert ObjectId to string for JSON serialization
            notification['_id'] = str(notification['_id'])

            # Convert created_at to dd/mm/yyyy format
            created_at = notification.get("created_at")
            if created_at:
                notification["created_at"] = convert_to_DMY_str(created_at)
            if user_id not in notification.get("seen_users", []):
                notification["is_seen"] = False
                del notification["seen_users"]
                notifications.append(notification)

        return notifications
    async def mark_as_read(self, user_id: int, notification_id: str) -> str:
        try:
            notification_object_id = ObjectId(notification_id)
        except errors.InvalidId:
            msg = notification_id
            raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_OBJECT_ID, description=msg)
        collection = db[COLLECTION_NAME]

        # Tìm và cập nhật thông báo cụ thể với notification_id
        notification = collection.find_one(
            {"_id": ObjectId(notification_object_id), "to_notify_users": {"$in": [user_id]}})

        if not notification:
            msg = notification_id
            logger.error(msg, exc_info=ValueError(AppStatus.ERROR_404_NOTIFICATION_NOT_FOUND))
            raise error_exception_handler(app_status=AppStatus.ERROR_404_NOTIFICATION_NOT_FOUND, description=msg)

        if user_id not in notification.get("seen_users", []):
            collection.update_one(
                {"_id": ObjectId(notification_id)},
                {"$addToSet": {"seen_users": user_id}}
            )

        return "Thông báo đã được đánh dấu là đã đọc"

    async def mark_all_as_read(self, user_id: int):
        collection = db[COLLECTION_NAME]

        # Update all notifications for the user by adding user_id to seen_users
        bulk_updates = []
        notifications_cursor = collection.find({"to_notify_users": {"$in": [user_id]}})
        for notification in notifications_cursor:
            if user_id not in notification.get("seen_users", []):
                bulk_updates.append(
                    UpdateOne(
                        {"_id": notification["_id"]},
                        {"$addToSet": {"seen_users": user_id}}
                    )
                )

        if bulk_updates:
            collection.bulk_write(bulk_updates)

        return "Tất cả thông báo đã được đánh dấu là đã đọc"