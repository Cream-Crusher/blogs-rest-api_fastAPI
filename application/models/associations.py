from sqlalchemy import Column, ForeignKey, Table

from application.database import Base


user_blogs_subscriptions = Table(
    'association_table_subscriptions',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('blog_id', ForeignKey('blogs.id'), primary_key=True),
)
