from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Provider
from .schemas import (
    Provider as ProviderSchema,
    ProviderCreate,
    ProviderUpdate,
)
from typing import List

router = APIRouter()


@router.post("/providers/", response_model=ProviderSchema)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    db_provider = Provider(**provider.dict())
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


@router.get("/providers/", response_model=List[ProviderSchema])
def read_providers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    providers = db.query(Provider).offset(skip).limit(limit).all()
    print(providers)
    return providers


@router.put("/providers/{provider_id}", response_model=ProviderSchema)
def update_provider(
    provider_id: int, provider: ProviderUpdate, db: Session = Depends(get_db)
):
    db_provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not db_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    for key, value in provider.dict().items():
        setattr(db_provider, key, value)
    db.commit()
    return db_provider


@router.delete("/providers/{provider_id}", response_model=ProviderSchema)
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not db_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    db.delete(db_provider)
    db.commit()
    return db_provider
