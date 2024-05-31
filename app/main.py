from fastapi import FastAPI

from app.auth.routers import router as AuthRouter

app = FastAPI()

app.include_router(AuthRouter, prefix="/users", tags=["user"])
