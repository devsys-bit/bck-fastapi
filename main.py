from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi_pagination import add_pagination
from database import engine
from task.controller import router
from datetime import datetime, timezone
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Código de inicialización (antes de que la app comience a servir requests)
  async with engine.begin() as conn:
    await conn.run_sync(SQLModel.metadata.create_all)
  yield
  # Código de finalización (cuando la app se está cerrando)
  await engine.dispose()

app = FastAPI(lifespan=lifespan)

add_pagination(app)

@app.get("/")
async def welcome():
  now = datetime.now(timezone.utc)
  return {
    "mensaje": "👋 Bienvenido a la API multi-task construida con FastAPI",
    "fechaHoraUTC": now.isoformat()  # estándar ISO 8601
  }

app.include_router(router)
