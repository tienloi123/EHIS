from app.cruds import BaseCRUD
from app.models import User
from app.schemas import UserCreate, UserUpdate


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    pass


user_crud = UserCRUD(User)
