from datetime import datetime
from typing import Optional, List
from fastapi_filter.contrib.sqlalchemy import Filter as SQLModelFilter
from .entity import Task

class FilterTask(SQLModelFilter):
  id__in: Optional[list[int]] = None
  title__ilike: Optional[str] = None
  description__ilike: Optional[str] = None
  completed: Optional[bool] = None
  created_at__gte: Optional[datetime] = None
  created_at__lte: Optional[datetime] = None
  created_at__ilike: Optional[str] = None
  updated_at__gte: Optional[datetime] = None
  updated_at__lte: Optional[datetime] = None
  updated_at__ilike: Optional[str] = None
  search: Optional[str] = None
  order_by: Optional[List[str]] = None

  class Constants(SQLModelFilter.Constants):
    model = Task
    ordering_field_name = "order_by"
    search_field_name = "search"
    search_model_fields = ["title", "description", "created_at", "updated_at"]
