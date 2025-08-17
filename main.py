from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi_pagination import add_pagination
from database import engine
from task.controller import router
from datetime import datetime, timezone

app = FastAPI()

add_pagination(app)

@app.on_event("startup")
async def on_startup():
  async with engine.begin() as conn:
    await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
async def welcome():
  now = datetime.now(timezone.utc)
  return {
    "mensaje": "👋 Bienvenido a la API multi-task construida con FastAPI",
    "fechaHoraUTC": now.isoformat()  # estándar ISO 8601
  }

app.include_router(router)
