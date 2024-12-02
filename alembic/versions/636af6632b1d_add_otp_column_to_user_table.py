"""add otp column to user table

Revision ID: 636af6632b1d
Revises: e9374e8e594f
Create Date: 2024-12-02 09:56:17.692130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '636af6632b1d'
down_revision: Union[str, None] = 'e9374e8e594f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('otp', sa.String(), nullable=True))

def downgrade() -> None:
    pass
