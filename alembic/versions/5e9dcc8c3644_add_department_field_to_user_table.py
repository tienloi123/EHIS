"""add department field to user table

Revision ID: 5e9dcc8c3644
Revises: ddd93d2eb558
Create Date: 2024-10-25 09:39:02.641600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e9dcc8c3644'
down_revision: Union[str, None] = 'ddd93d2eb558'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'department' column to 'user' table
    op.add_column('user', sa.Column('department', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'department')
