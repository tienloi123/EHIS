import json
import logging
from datetime import datetime, date
from typing import Dict, Any, List, Type
from urllib.parse import unquote

import pytz

logger = logging.getLogger(__name__)


def convert_str_DMY_to_date_time(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%H:%M:%S %d/%m/%Y")

def convert_str_DMY_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%d/%m/%Y").date()

def convert_to_DMY_str(date_value):
    if date_value is None:
        return None  # or return a default string like 'N/A'
    return date_value.strftime('%d/%m/%Y')


def convert_str_to_param(param: str):
    decoded_param = unquote(param)
    param_data = json.loads(decoded_param)
    return param_data


def convert_date_to_datetime(date_value: date) -> datetime:
    return datetime(date_value.year, date_value.month, date_value.day)


def convert_dates(notification: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    for field in fields:
        date_value = notification.get(field)
        if date_value:
            notification[field] = convert_to_DMY_str(date_value)
    return notification


def convert_datetime_to_str(datetime_value: datetime) -> str:
    # Đặt múi giờ ban đầu là UTC
    utc_datetime = datetime_value.replace(tzinfo=pytz.utc)
    # Chuyển đổi sang múi giờ UTC+7
    utc_plus_7 = utc_datetime.astimezone(pytz.timezone('Asia/Bangkok'))
    return utc_plus_7.strftime("%H:%M:%S %d/%m/%Y")

def convert_datetime_to_date_str(datetime_value: datetime) -> str:
    return datetime_value.strftime("%d/%m/%Y")

def convert_datetime_to_time_str(datetime_value: datetime) -> str:
    # Đặt múi giờ ban đầu là UTC
    utc_datetime = datetime_value.replace(tzinfo=pytz.utc)
    # Chuyển đổi sang múi giờ UTC+7
    utc_plus_7 = utc_datetime.astimezone(pytz.timezone('Asia/Bangkok'))
    return utc_plus_7.strftime("%H:%M:%S")


def convert_to_vietnam_time(utc_datetime):
    """
    Chuyển đổi datetime từ UTC sang múi giờ Việt Nam (UTC+7)

    :param utc_datetime: datetime hoặc chuỗi datetime (UTC)
    :return: datetime trong múi giờ Việt Nam hoặc None nếu không hợp lệ
    """
    if not utc_datetime:
        return None

    try:
        # Nếu utc_datetime là chuỗi, chuyển sang đối tượng datetime
        if isinstance(utc_datetime, str):
            utc_datetime = datetime.fromisoformat(utc_datetime.replace("Z", "+00:00"))

        # Chuyển đổi datetime sang múi giờ UTC
        utc = pytz.utc.localize(utc_datetime)

        # Chuyển đổi từ UTC sang múi giờ Việt Nam (Asia/Ho_Chi_Minh)
        vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        vietnam_time = utc.astimezone(vietnam_tz)

        return vietnam_time
    except Exception as e:
        print(f"Lỗi khi chuyển đổi datetime: {e}")
        return None