from application.routes import user_route, blog_route, post_route, tag_route, comment_route

from fastapi import FastAPI

app = FastAPI()

app.include_router(user_route.router)
app.include_router(blog_route.router)
app.include_router(post_route.router)
app.include_router(tag_route.router)
app.include_router(comment_route.router)