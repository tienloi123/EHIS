from sqlalchemy import Column, String, DateTime, Integer

from . import Base


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    patient_name = Column(String(), nullable=False)
    patient_phone_number = Column(String(), nullable=False)
    test_date = Column(DateTime(timezone=True), nullable=False)
    result_test = Column(String, nullable=False)
    def dict(self):
        result = self.to_dict()
        return result
