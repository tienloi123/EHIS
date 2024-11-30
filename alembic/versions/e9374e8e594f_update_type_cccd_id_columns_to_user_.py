"""update type cccd_id columns to user table

Revision ID: e9374e8e594f
Revises: 047b2227cbae
Create Date: 2024-11-25 10:32:15.903203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9374e8e594f'
down_revision: Union[str, None] = '047b2227cbae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('user', 'cccd_id', existing_type=sa.Integer(), type_=sa.BigInteger(), nullable=True)

def downgrade():
    op.alter_column('user', 'cccd_id', existing_type=sa.BigInteger(), type_=sa.Integer(), nullable=True)
