"""add medical_record column to appointment table

Revision ID: 47ae6b76f7d9
Revises: 92a7fb9032c9
Create Date: 2024-11-17 16:58:50.283548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47ae6b76f7d9'
down_revision: Union[str, None] = '92a7fb9032c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Thêm cột mới 'medical_record' vào bảng 'appointment'
    op.add_column('appointment', sa.Column('medical_record', sa.Integer(), nullable=True))


def downgrade():
    # Xóa cột 'medical_record' khỏi bảng 'appointment' nếu rollback migration
    op.drop_column('appointment', 'medical_record')
