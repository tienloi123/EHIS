import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.patient_crud import patient_crud

logger = logging.getLogger(__name__)


class PatientService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_patients(self, offset: int, limit: int):
        data = []
        patients = await patient_crud.get_multi(
            self.session,
            offset=offset,
            limit=limit
        )
        for patient in patients:
            data.append(patient.dict())
        return data