"""create medical_record_doctor table

Revision ID: 22cf04900afb
Revises: 3f624078474e
Create Date: 2024-11-13 15:16:12.864601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22cf04900afb'
down_revision: Union[str, None] = 'a922dab39786'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Tạo bảng medical_record_doctor
    op.create_table(
        'medical_record_doctor',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('medical_record_id', sa.Integer, nullable=False),  # ID của bản ghi khám
        sa.Column('diagnosis', sa.String, nullable=True),            # Chẩn đoán
        sa.Column('prescription', sa.String, nullable=True),         # Đơn thuốc
        sa.Column('payment_amount', sa.Float, nullable=True)         # Số tiền thanh toán
    )

def downgrade():
    # Xóa bảng medical_record_doctor nếu rollback migration
    op.drop_table('medical_record_doctor')
