"""update user model with amount

Revision ID: 13633e011de9
Revises: 7a862e865e4f
Create Date: 2024-01-20 16:24:49.255440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13633e011de9'
down_revision: Union[str, None] = '7a862e865e4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
