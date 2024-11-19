import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import lab_test_crud
from app.schemas import LabTestRequest, LabTestCreate

logger = logging.getLogger(__name__)


class LabTestService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_lab_test(self, lab_test_data: LabTestRequest):
        test_date = datetime.utcnow()
        lab_test_data = await lab_test_crud.create(self.session, obj_in=LabTestCreate(
            medical_record_doctor_id=lab_test_data.medical_record_doctor_id,
            test_name=lab_test_data.test_name,
            department=lab_test_data.department, result_test=lab_test_data.result_test, test_date=test_date))

        return lab_test_data.dict()
