"""add cccd_id and residence columns to user table

Revision ID: 047b2227cbae
Revises: 3d631bc0565f
Create Date: 2024-11-25 10:08:46.277414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '047b2227cbae'
down_revision: Union[str, None] = '3d631bc0565f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'cccd_id' and 'residence' columns to 'user' table
    op.add_column('user', sa.Column('cccd_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('residence', sa.String(), nullable=True))


def downgrade() -> None:
    # Drop 'cccd_id' and 'residence' columns from 'user' table
    op.drop_column('user', 'cccd_id')
    op.drop_column('user', 'residence')
