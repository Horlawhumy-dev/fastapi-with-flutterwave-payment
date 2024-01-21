"""Add role column to user

Revision ID: bd1e289e4334
Revises: 14a8a92a91d2
Create Date: 2024-01-20 16:50:17.922426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from enum import Enum as PythonEnum, auto


# revision identifiers, used by Alembic.
revision: str = 'bd1e289e4334'
down_revision: Union[str, None] = '14a8a92a91d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class UserRole(PythonEnum):
    SENDER = 'SENDER'
    RIDER = 'RIDER'
    ADMIN = 'ADMIN'


user_role_enum = sa.Enum(UserRole, name='userrole', create_type=True)

def upgrade() -> None:
    op.add_column('user', sa.Column('role', user_role_enum, server_default=UserRole.SENDER.value, nullable=False))


def downgrade() -> None:
    op.drop_column('user', 'role')
