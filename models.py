from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    user_id: str
    name: str
    price: str


class ItemUpdate(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None
    price: Optional[str] = None
