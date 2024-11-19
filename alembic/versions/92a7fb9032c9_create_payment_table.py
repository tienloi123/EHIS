"""create payment table

Revision ID: 92a7fb9032c9
Revises: ddd93d2eb558
Create Date: 2024-11-13 15:37:41.661989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92a7fb9032c9'
down_revision: Union[str, None] = 'ddd93d2eb558'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Tạo bảng payment
    op.create_table(
        'payment',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('medical_record_id', sa.Integer, sa.ForeignKey('medical_record.id', ondelete="SET NULL"), nullable=True),  # ID của hồ sơ y tế
        sa.Column('amount', sa.Float, nullable=False),  # Số tiền thanh toán
        sa.Column('status', sa.Enum('PENDING', 'COMPLETED', 'FAILED', name='status_payment_enum'), nullable=False, server_default='PENDING'),  # Trạng thái thanh toán
        sa.Column('payment_date', sa.DateTime(timezone=True), server_default=sa.func.timezone('Asia/Ho_Chi_Minh', sa.func.now())),  # Ngày thanh toán
    )

def downgrade():
    # Xóa bảng payment nếu rollback migration
    op.drop_table('payment')
    # Xóa enum type nếu cần
    op.execute('DROP TYPE status_payment_enum')
