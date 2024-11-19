from app.cruds import BaseCRUD
from app.models.Payment import Payment
from app.schemas import PaymentCreate, PaymentUpdate


class PaymentCRUD(BaseCRUD[Payment, PaymentCreate, PaymentUpdate]):
    pass


payment_crud = PaymentCRUD(Payment)
