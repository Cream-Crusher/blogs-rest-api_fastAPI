from application.routes import user, blog


from fastapi import FastAPI

app = FastAPI()

app.include_router(user.router)
app.include_router(blog.router)
