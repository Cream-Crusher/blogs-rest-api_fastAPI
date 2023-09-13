"""Create user and blog table

Revision ID: 33b4fe5479bc
Revises: 43491a145187
Create Date: 2023-09-13 15:22:35.830244

"""
from typing import Sequence, Union

from sqlalchemy import Integer, String, Column, Boolean, DateTime, func

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33b4fe5479bc'
down_revision: Union[str, None] = '43491a145187'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'blogs',
        Column('id', Integer, autoincrement=True, primary_key=True),
        Column('title', String(50)),
        Column('description', String(150), unique=True, index=True),
        Column('created_at', DateTime, server_default=func.now()),
        Column('updated_at', DateTime, onupdate=func.now())
    )

    op.create_table(
        'users',
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('username', String, index=True),
        Column('email', String, unique=True, index=True),
        Column('password', String),
        Column('is_active', Boolean, default=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('blogs')
