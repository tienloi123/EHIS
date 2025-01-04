import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.doctor_crud import doctors_crud

logger = logging.getLogger(__name__)


class DoctorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_doctors(self, offset: int, limit: int):
        data = []
        doctors = await doctors_crud.get_multi(
            self.session,
            offset=offset,
            limit=limit
        )
        for doctor in doctors:
            data.append(doctor.dict())
        return data