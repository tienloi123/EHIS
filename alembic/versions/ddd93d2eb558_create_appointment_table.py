"""create appointment table

Revision ID: ddd93d2eb558
Revises: c4af632d1f6b
Create Date: 2024-10-23 10:33:00.988155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddd93d2eb558'
down_revision: Union[str, None] = 'c4af632d1f6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Lệnh tạo bảng 'appointment'
    op.create_table(
        'appointment',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=True),
        sa.Column('doctor_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('status', sa.Enum('UNPROCESSED', 'PROCESSED', name='status_appointment_enum'), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.timezone('Asia/Ho_Chi_Minh', sa.func.now())),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.timezone('Asia/Ho_Chi_Minh', sa.func.now()), onupdate=sa.func.timezone('Asia/Ho_Chi_Minh', sa.func.now()))
    )


def downgrade():
    # Lệnh xóa bảng 'appointment' nếu rollback migration
    op.drop_table('appointment')

    # Xóa enum type nếu cần
    op.execute('DROP TYPE status_appointment_enum')
