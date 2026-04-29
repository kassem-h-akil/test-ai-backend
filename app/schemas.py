from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    description: str = ""


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ItemRead(ItemBase):
    id: int
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)
