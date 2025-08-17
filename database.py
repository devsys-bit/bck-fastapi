from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

"""
DATABASE_URL = (
  f"mysql+aiomysql://"
  f"{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}"
  f"@{os.getenv('HOST_DB')}:{os.getenv('PORT_DB')}"
  f"/{os.getenv('NAME_DB')}"
)
"""
DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}"
    f"@{os.getenv('HOST_DB')}:{os.getenv('PORT_DB')}"
    f"/{os.getenv('NAME_DB')}"
)


engine = create_async_engine(
  DATABASE_URL,
  echo=True,
  connect_args={"statement_cache_size": 0}
)

async def get_session() -> AsyncSession:
  async with AsyncSession(engine) as session:
    yield session
