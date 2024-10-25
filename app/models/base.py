from datetime import date, datetime
from typing import List

from sqlalchemy.orm import DeclarativeBase

from app.utils.covert_util import convert_to_DMY_str, convert_datetime_to_str


class Base(DeclarativeBase):
    def to_dict(self, un_selects: List[str] = None):
        result = {}
        for column in self.__table__.columns:
            if not un_selects or column.name not in un_selects:
                result[column.name] = getattr(self, column.name)
                if isinstance(result[column.name], datetime):
                    result[column.name] = convert_datetime_to_str(result[column.name])
                elif isinstance(result[column.name], date):
                    result[column.name] = convert_to_DMY_str(result[column.name])
        return result
