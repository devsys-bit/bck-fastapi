from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends
from database import get_session
from .dto import FilterTask
from .service import (
  findAll as find_all_service,
  findOne as find_one_service,
  create as create_service,
  update as update_service,
  remove as remove_service,
  restore as restore_service
)
from .entity import Task

router = APIRouter()

@router.get("/task", response_model=Page[Task])
async def findAll(filters: FilterTask = FilterDepends(FilterTask), session: AsyncSession = Depends(get_session)):
  return await find_all_service(session, filters)

@router.get("/task/{id}", response_model=Task)
async def findOne(id: int, session: AsyncSession = Depends(get_session)):
  return await find_one_service(session, id)

@router.post("/task/create", response_model=Task)
async def create(data: Task, session: AsyncSession = Depends(get_session)):
  return await create_service(session, data)

@router.patch("/task/update/{id}", response_model=Task)
async def update(id: int, data: dict, session: AsyncSession = Depends(get_session)):
  return await update_service(session, id, data)

@router.delete("/task/remove/{id}", response_model=Task)
async def remove(id: int, session: AsyncSession = Depends(get_session)):
  return await remove_service(session, id)

@router.patch("/task/restore/{id}", response_model=Task)
async def restore(id: int, session: AsyncSession = Depends(get_session)):
  return await restore_service(session, id)
