"""create superuser

Revision ID: c4af632d1f6b
Revises: d7cb6b4fe146
Create Date: 2024-09-26 19:13:05.302361

"""
from typing import Sequence, Union
from datetime import datetime
import sqlalchemy as sa
from alembic import op

from app.utils import hash_password

# revision identifiers, used by Alembic.
revision: str = 'c4af632d1f6b'
down_revision: Union[str, None] = 'd7cb6b4fe146'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    email = "admin@gmail.com"
    password = "123"
    hashed_password = hash_password(password)
    name = "Admin"
    dob = datetime(2002, 7, 2)

    op.execute(
        sa.text(
            'INSERT INTO "user" (email, name, dob, hashed_password, role, gender) VALUES '
            '(:email, :name, :dob, :hashed_password, :role, :gender)'
        ).bindparams(
            email=email,
            name=name,
            dob=dob,
            hashed_password=hashed_password,
            role='Superuser',
            gender='Nam'
        )
    )

    print("Superuser:: email = ", email)
    print("Superuser:: password = ", password)


def downgrade() -> None:
    pass
