from sqlmodel import select
from fastapi_pagination.ext.sqlmodel import paginate as sqlmodel_paginate
from fastapi_pagination import Page
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.exc import NoResultFound
from .dto import FilterTask
from .entity import Task

async def findAll(session: AsyncSession, filters: FilterTask) -> Page[Task]:
  query = select(Task).where(Task.deleted_at.is_(None))
  query = filters.sort(query)
  query = filters.filter(query)
  return await sqlmodel_paginate(session, query)

async def findOne(session: AsyncSession, task_id: int) -> Task:
  result = await session.execute(
    select(Task).where(Task.id == task_id, Task.deleted_at.is_(None))
  )
  task = result.scalar_one_or_none()
  if not task:
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
  return task

async def create(session: AsyncSession, data: Task) -> Task:
  session.add(data)
  await session.commit()
  await session.refresh(data)
  return data

async def update(session: AsyncSession, task_id: int, data: dict) -> Task:
  task = await findOne(session, task_id)
  for key, value in data.items():
    setattr(task, key, value)
  task.updated_at = datetime.utcnow()
  session.add(task)
  await session.commit()
  await session.refresh(task)
  return task

async def remove(session: AsyncSession, task_id: int) -> Task:
  task = await findOne(session, task_id)
  task.deleted_at = datetime.utcnow()
  session.add(task)
  await session.commit()
  await session.refresh(task)
  return task

async def restore(session: AsyncSession, task_id: int) -> Task:
  result = await session.execute(select(Task).where(Task.id == task_id, Task.deleted_at.is_not(None)))
  task = result.scalar_one_or_none()
  if not task:
    raise NoResultFound(f"Deleted Task {task_id} not found")
  task.deleted_at = None
  task.updated_at = datetime.utcnow()
  session.add(task)
  await session.commit()
  await session.refresh(task)
  return task
