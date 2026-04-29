from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Item
from ..schemas import ItemCreate, ItemRead


router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
def list_items(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by name (substring, case-insensitive)"),
    description: Optional[str] = Query(None, description="Filter by description (substring)"),
    created_from: Optional[datetime] = Query(None, description="Items created on/after this datetime"),
    created_to: Optional[datetime] = Query(None, description="Items created on/before this datetime"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    stmt = select(Item)

    if name:
        stmt = stmt.where(Item.name.ilike(f"%{name}%"))
    if description:
        stmt = stmt.where(Item.description.ilike(f"%{description}%"))
    if created_from:
        stmt = stmt.where(Item.created_date >= created_from)
    if created_to:
        stmt = stmt.where(Item.created_date <= created_to)

    stmt = stmt.order_by(Item.created_date.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()


@router.post("", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    item = Item(name=payload.name, description=payload.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
