"""update user model with role type

Revision ID: 14a8a92a91d2
Revises: 13633e011de9
Create Date: 2024-01-20 16:35:30.317142

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14a8a92a91d2'
down_revision: Union[str, None] = '13633e011de9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
