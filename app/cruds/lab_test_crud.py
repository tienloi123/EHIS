from app.cruds import BaseCRUD
from app.models.LabTest import LabTest
from app.schemas import LabTestCreate


class LabTestCRUD(BaseCRUD[LabTest, LabTestCreate, LabTestCreate]):
    pass


lab_test_crud = LabTestCRUD(LabTest)
