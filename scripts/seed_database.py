# from src.database import
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import Provider, ServiceArea
from shapely.geometry import Polygon
from faker import Faker
import random
from geoalchemy2 import WKTElement

fake = Faker()


# Function to generate a random polygon/rectangle
def generate_random_polygon():
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    offset = random.uniform(2.0, 30.0)
    return Polygon(
        [
            (lon, lat),
            (lon + offset, lat),
            (lon + offset, lat + offset),
            (lon, lat + offset),
            (lon, lat),
        ]
    )


def seed_database(n_providers=100, n_service_areas=300):
    db: Session = SessionLocal()

    try:
        providers = []
        for _ in range(n_providers):
            provider = Provider(
                name=fake.company(),
                email=f"{fake.user_name()}@gmail.com",
                language=fake.random_element(
                    elements=("en", "fr", "es", "de", "ar")
                ),  # ISO language codes
                currency=fake.random_element(
                    elements=("USD", "EUR", "GBP", "JPY", "CAD")
                ),
            )
            providers.append(provider)

        db.add_all(providers)
        db.commit()

        service_areas = []
        for _ in range(n_service_areas):
            polygon = generate_random_polygon()
            service_area = ServiceArea(
                name=f"{fake.city()} Service Area",
                price=round(
                    random.uniform(10.0, 500.0), 2
                ),  # Generate a random price between 10 and 500
                geojson=WKTElement(polygon.wkt, srid=4326),
            )
            service_areas.append(service_area)

        db.add_all(service_areas)

        db.commit()
        print(
            f"Database seeded with {n_providers} providers and {n_service_areas} service areas."
        )

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
