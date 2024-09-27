# PolygonFinder

Helps you keep track of Service Areas and determine whether a geo point falls within any of your service areas.

## Architecture

- **PostgreSQL** with PostGIS extensions
- **FastAPI** as the web framework
- **SQLAlchemy** as the ORM
- **GeoAlchemy2** for managing geo data format
- **Alembic** for database schema migrations

## Requirements

- Python 3.10
- Docker & Docker Compose

## Getting Started

1. **Run the Postgres Database**:
    ```bash
    docker-compose up -d
    ```

2. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    ```bash
    cp .env.sample .env
    ```

4. **Apply database migrations**:
    ```bash
    alembic upgrade head
    ```

5. **Run the application**:
    ```bash
    uvicorn src.main:app --reload
    ```

## Endpoints

- **Providers**:
    - `GET /providers`: List all providers
    - `POST /providers`: Create a new provider
    - `GET /providers/{id}`: Get details of a provider
    - `PUT /providers/{id}`: Update a provider
    - `DELETE /providers/{id}`: Delete a provider

- **Service Areas**:
    - `GET /service-areas`: List all service areas
    - `POST /service-areas`: Create a new service area
    - `GET /service-areas/{id}`: Get details of a service area
    - `PUT /service-areas/{id}`: Update a service area
    - `DELETE /service-areas/{id}`: Delete a service area
    - `GET /service-areas/search?lat={latitude}&lng={longitude}`: Find service areas containing a specific geo point

## Testing

To run tests:
```bash
pytest
```

## Deployment
