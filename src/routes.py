from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import mapping, shape
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Provider, ServiceArea
from .schemas import (
    Provider as ProviderSchema,
    ServiceArea as ServiceAreaSchema,
    ProviderCreate,
    ProviderUpdate,
    ServiceAreaCreate,
    ServiceAreaUpdate,
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


# Utility function to convert WKBElement to GeoJSON string
def service_area_to_dict(service_area):
    geojson_response = mapping(to_shape(service_area.geojson))
    return {
        "id": service_area.id,
        "name": service_area.name,
        "price": service_area.price,
        "geojson": json.dumps(geojson_response)  # Convert to valid GeoJSON string
    }


@router.post("/serviceareas/", response_model=ServiceAreaSchema)
def create_service_area(service_area: ServiceAreaCreate, db: Session = Depends(get_db)):
    geojson_dict = json.loads(service_area.geojson)
    geometry = shape(geojson_dict)

    # Check that the geometry is a Polygon
    if geometry.geom_type != "Polygon":
        raise HTTPException(status_code=400, detail="GeoJSON must represent a POLYGON")

    # Create the ServiceArea instance and convert the geometry to WKB format for database storage
    db_service_area = ServiceArea(
        name=service_area.name,
        price=service_area.price,
        geojson=from_shape(geometry, srid=4326)  # Store the geometry in WKB format with SRID 4326
    )
    db.add(db_service_area)
    db.commit()
    db.refresh(db_service_area)

    return service_area_to_dict(db_service_area)


@router.get("/serviceareas/", response_model=List[ServiceAreaSchema])
def read_service_areas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service_areas = db.query(ServiceArea).offset(skip).limit(limit).all()
    return [service_area_to_dict(sa) for sa in service_areas]


@router.put("/serviceareas/{service_area_id}", response_model=ServiceAreaSchema)
def update_service_area(
    service_area_id: int, service_area: ServiceAreaUpdate, db: Session = Depends(get_db)
):
    db_service_area = db.query(ServiceArea).filter(ServiceArea.id == service_area_id).first()
    if not db_service_area:
        raise HTTPException(status_code=404, detail="Service area not found")
    for key, value in service_area.dict().items():
        setattr(db_service_area, key, value)
    db.commit()

    return service_area_to_dict(db_service_area)


@router.delete("/serviceareas/{service_area_id}", response_model=ServiceAreaSchema)
def delete_service_area(service_area_id: int, db: Session = Depends(get_db)):
    db_service_area = db.query(ServiceArea).filter(ServiceArea.id == service_area_id).first()
    if not db_service_area:
        raise HTTPException(status_code=404, detail="Service area not found")
    db.delete(db_service_area)
    db.commit()

    return service_area_to_dict(db_service_area)
