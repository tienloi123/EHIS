"""add avatar_url field to user table

Revision ID: 77a576a00220
Revises: 636af6632b1d
Create Date: 2024-12-16 15:18:51.991998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77a576a00220'
down_revision: Union[str, None] = '636af6632b1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Thêm cột avatar_url vào bảng user
    op.add_column('user', sa.Column('avatar_url', sa.String(), nullable=True))


def downgrade():
    # Xóa cột avatar_url khi rollback
    op.drop_column('user', 'avatar_url')
