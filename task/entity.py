from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True, index=True)
  title: Optional[str] = Field(default="", max_length=50)
  description: Optional[str] = Field(default="", max_length=100)
  completed: Optional[bool] = Field(default=False)
  created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
  updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
  deleted_at: Optional[datetime] = Field(default=None, nullable=True)
