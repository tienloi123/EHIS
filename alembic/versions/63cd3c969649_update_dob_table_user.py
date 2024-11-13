"""update dob table user

Revision ID: 63cd3c969649
Revises: fca6e93efce5
Create Date: 2024-11-01 15:27:43.889387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63cd3c969649'
down_revision: Union[str, None] = 'fca6e93efce5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user', 'dob', type_=sa.Date(), existing_type=sa.DateTime(), nullable=False)


def downgrade() -> None:
    pass
