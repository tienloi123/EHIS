import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import receptionist_crud

logger = logging.getLogger(__name__)


class ReceptionistService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_receptionists(self, offset: int, limit: int):
        data = []
        receptionists = await receptionist_crud.get_multi(
            self.session,
            offset=offset,
            limit=limit
        )
        for receptionist in receptionists:
            data.append(receptionist.dict())
        return data
