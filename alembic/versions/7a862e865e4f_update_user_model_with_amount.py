"""update user model with amount

Revision ID: 7a862e865e4f
Revises: f70bbb0a94a4
Create Date: 2024-01-20 15:17:50.043202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a862e865e4f'
down_revision: Union[str, None] = 'f70bbb0a94a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
