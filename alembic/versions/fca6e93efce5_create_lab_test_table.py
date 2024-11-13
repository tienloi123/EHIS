"""create lab_test table

Revision ID: fca6e93efce5
Revises: a922dab39786
Create Date: 2024-10-30 14:37:11.131941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fca6e93efce5'
down_revision: Union[str, None] = 'a922dab39786'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'lap_test',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_id', sa.Integer, sa.ForeignKey('user.id', ondelete="CASCADE"), nullable=False),
        sa.Column('doctor_id', sa.Integer, sa.ForeignKey('user.id', ondelete="CASCADE"), nullable=False),
        sa.Column('medical_record_id', sa.Integer, sa.ForeignKey('medical_record.id', ondelete="CASCADE"), nullable=False),
        sa.Column('test_name', sa.String(), nullable=False),
        sa.Column('department', sa.String, nullable=False),
        sa.Column('test_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('result_test', sa.String, nullable=False),
    )

def downgrade():
    op.drop_table('lap_test')
