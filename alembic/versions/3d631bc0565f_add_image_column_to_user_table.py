"""add image column to user table

Revision ID: 3d631bc0565f
Revises: 81b659423331
Create Date: 2024-11-20 14:05:56.930382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d631bc0565f'
down_revision: Union[str, None] = '81b659423331'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('medical_record', sa.Column('image', sa.String(), nullable=True))


def downgrade() -> None:
    pass
