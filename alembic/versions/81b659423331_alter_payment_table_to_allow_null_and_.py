"""alter payment table to allow null and remove default for payment_date

Revision ID: 81b659423331
Revises: 47ae6b76f7d9
Create Date: 2024-11-20 11:06:48.148150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81b659423331'
down_revision: Union[str, None] = '47ae6b76f7d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Sửa đổi cột payment_date để có thể nhận NULL và không có giá trị mặc định
    op.alter_column(
        'payment', 'payment_date',
        nullable=True,  # Cho phép giá trị NULL
        server_default=None  # Xóa giá trị mặc định
    )


def downgrade() -> None:
    pass
