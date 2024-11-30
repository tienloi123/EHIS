"""add embedding column to user table

Revision ID: eadc65a30bc5
Revises: e9374e8e594f
Create Date: 2024-11-27 08:27:25.773550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eadc65a30bc5'
down_revision: Union[str, None] = 'e9374e8e594f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the 'embedding' column
    op.add_column(
        'user',
        sa.Column('embedding', sa.JSON(), nullable=True)
    )


def downgrade() -> None:
    # Remove the 'embedding' column
    op.drop_column('user', 'embedding')
