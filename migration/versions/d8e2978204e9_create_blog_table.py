"""Create blog table

Revision ID: d8e2978204e9
Revises: 59e62ae9e4d6
Create Date: 2023-09-12 20:54:20.678345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8e2978204e9'
down_revision: Union[str, None] = '59e62ae9e4d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
