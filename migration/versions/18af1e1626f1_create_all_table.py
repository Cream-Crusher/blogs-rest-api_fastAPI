"""Create all table

Revision ID: 18af1e1626f1
Revises: 90fb29239cb1
Create Date: 2023-09-18 15:48:23.335955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, DateTime, String, func, Boolean, ForeignKey
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '18af1e1626f1'
down_revision: Union[str, None] = '90fb29239cb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('username', String, index=True),
        Column('email', String, unique=True, index=True),
        Column('password', String),
        Column('is_active', Boolean, default=True)
    )
    op.create_table(
        'blogs',
        Column('id', Integer, autoincrement=True, primary_key=True),
        Column('title', String(50)),
        Column('description', String(150), unique=True, index=True),
        Column('created_at', DateTime, server_default=func.now()),
        Column('updated_at', DateTime, onupdate=func.now())
    )
    op.create_table(
        'tags',
        Column('id', Integer, autoincrement=True, primary_key=True),
        Column('tag_name', String(50), unique=True)
    )
    op.create_table(
        'posts',
        Column('id', Integer, autoincrement=True, primary_key=True),
        Column('title', String(50), index=True),
        Column('body', String),
        Column('is_published', Boolean, default=False),
        Column('created_at', DateTime, server_default=func.now()),
        Column('views', Integer, default=0)
    )
    op.create_table(
        'comments',
        Column('id', Integer, autoincrement=True, primary_key=True),
        Column('body', String),
        Column('created_at', DateTime, server_default=func.now()),

    )
    op.create_table(
        'association_table_subscriptions',
        Column('user_id', sa.Integer, ForeignKey('users.id'), primary_key=True),
        Column('blog_id', sa.Integer, ForeignKey('blogs.id'), primary_key=True),
    )


def downgrade() -> None:
    pass