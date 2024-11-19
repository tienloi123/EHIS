from sqlalchemy import Column, Integer, String, DateTime

from . import Base


class LabTest(Base):
    __tablename__ = "lap_test"

    id = Column(Integer, primary_key=True)
    medical_record_doctor_id = Column(Integer, nullable=False)  # ID của bản ghi khám của bác sĩ
    test_name = Column(String, nullable=False)  # Tên xét nghiệm
    department = Column(String, nullable=False)  # Phòng ban thực hiện xét nghiệm
    test_date = Column(DateTime(timezone=True), nullable=False)  # Ngày thực hiện xét nghiệm
    result_test = Column(String, nullable=False)  # Kết quả xét nghiệm

    def dict(self):
        result = self.to_dict()
        return result

