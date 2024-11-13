"""add clinic location field to user table 

Revision ID: 3f624078474e
Revises: 63cd3c969649
Create Date: 2024-11-03 22:37:57.922250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f624078474e'
down_revision: Union[str, None] = '63cd3c969649'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'department' column to 'user' table
    op.add_column('user', sa.Column('clinic_location', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'department')