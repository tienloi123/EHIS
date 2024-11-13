"""create user table

Revision ID: d7cb6b4fe146
Revises: 
Create Date: 2024-09-26 19:05:01.757158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = 'd7cb6b4fe146'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the 'user' table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), unique=True, nullable=False),
        sa.Column('name', sa.String(length=45), nullable=False),
        sa.Column('dob', sa.DateTime(timezone=True), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('Superuser', 'Doctor', 'Receptionist', 'Patient', name='role_enum'), nullable=False),
        sa.Column('gender', sa.Enum('Nam', 'Nữ', 'Khác', name='gender_enum'), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=func.timezone('Asia/Ho_Chi_Minh', func.now())),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=func.timezone('Asia/Ho_Chi_Minh', func.now()),
                  onupdate=func.timezone('Asia/Ho_Chi_Minh', func.now())),
        sa.Column('access_token', sa.String(), nullable=True),
        sa.Column('refresh_token', sa.String(), nullable=True),
    )


def downgrade() -> None:
    # Drop the 'user' table
    op.drop_table('user')
