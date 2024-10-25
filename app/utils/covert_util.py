import json
import logging
from datetime import datetime, date
from typing import Dict, Any, List
from urllib.parse import unquote

logger = logging.getLogger(__name__)


def convert_str_DMY_to_date_time(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%H:%M:%S %d/%m/%Y")


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
    return datetime_value.strftime("%H:%M:%S %d/%m/%Y")
