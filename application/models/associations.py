from sqlalchemy import Column, ForeignKey, Table

from application.database import Base


user_blogs_subscriptions = Table(
    'association_table_subscriptions',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('blog_id', ForeignKey('blogs.id'), primary_key=True),
)

user_blogs_authors = Table(
    'association_table_authors',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('blog_id', ForeignKey('blogs.id'), primary_key=True),
)

post_tags = Table(
    'association_table_tags',
    Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)

users_post_likes = Table(
    'association_table_likes',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
)
