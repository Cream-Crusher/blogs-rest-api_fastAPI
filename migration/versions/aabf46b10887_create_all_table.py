"""Create all table

Revision ID: aabf46b10887
Revises: b6920ffebbf4
Create Date: 2023-09-20 21:53:04.647349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

# revision identifiers, used by Alembic.
revision: str = 'aabf46b10887'
down_revision: Union[str, None] = 'b6920ffebbf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        Column('id', Integer, autoincrement=True, primary_key=True),
        Column('username', String, index=True),
        Column('email', String, unique=True, index=True),
        Column('password', String),
        Column('is_active', Boolean, default=True)
    )
    op.create_table('posts',
        Column('id', Integer, autoincrement=True, primary_key=True),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('body', sa.String(), nullable=False),
        sa.Column('is_published', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('views', sa.Integer(), default=0),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    )
    op.create_table('blogs',
        Column('id', Integer, autoincrement=True, primary_key=True),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=150), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now()),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    )

    op.create_table(
        'tags',
        Column('id', Integer, autoincrement=True, primary_key=True),
        Column('tag_name', String(50), unique=True)
    )
    op.create_table('comments',
        Column('id', Integer, autoincrement=True, primary_key=True),
        sa.Column('body', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
                    )

    op.create_table(
        'association_table_subscriptions',
        Column('user_id', sa.Integer, ForeignKey('users.id'), primary_key=True),
        Column('blog_id', sa.Integer, ForeignKey('blogs.id'), primary_key=True),
    )
    op.create_table('association_table_authors',
        Column('user_id', sa.Integer, ForeignKey('users.id'), primary_key=True),
        Column('blog_id', sa.Integer, ForeignKey('blogs.id'), primary_key=True),
    )
    op.create_table('association_table_tags',
        Column('post_id', sa.Integer, ForeignKey('posts.id'), primary_key=True),
        Column('tag_id', sa.Integer, ForeignKey('tags.id'), primary_key=True),
    )
    op.create_table('association_table_likes',
        Column('user_id', sa.Integer, ForeignKey('users.id'), primary_key=True),
        Column('post_id', sa.Integer, ForeignKey('posts.id'), primary_key=True),
    )

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
