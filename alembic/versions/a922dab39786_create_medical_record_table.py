"""create medical_record table

Revision ID: a922dab39786
Revises: 5e9dcc8c3644
Create Date: 2024-10-30 14:35:41.684775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a922dab39786'
down_revision: Union[str, None] = '5e9dcc8c3644'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.create_table(
        'medical_record',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_id', sa.Integer, sa.ForeignKey('user.id', ondelete="CASCADE"), nullable=True),
        sa.Column('doctor_id', sa.Integer, sa.ForeignKey('user.id', ondelete="CASCADE"), nullable=True),
        sa.Column('appointment_id', sa.Integer, sa.ForeignKey('appointment.id', ondelete="CASCADE"), nullable=True),
        sa.Column('diagnosis', sa.String, nullable=True),
        sa.Column('prescription', sa.String, nullable=True),
        sa.Column('visit_date', sa.DateTime(timezone=True), server_default=sa.func.timezone('Asia/Ho_Chi_Minh', sa.func.now())),
        sa.Column('notes', sa.String, nullable=True),
    )

def downgrade():
    op.drop_table('medical_record')
