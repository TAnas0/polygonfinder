# PolygonFinder

This REST API helps you keep track of Service Areas and determine whether a geo point falls within any of your service areas.

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

You can quickly get started by running a single command: `docker-compose up -d`.
This will launch a Postgres database with PostGIS installed, apply Alembic migrations on the database and serve the API.

If you wish to run the API locally for the sake of easier development and debugging, you can proceed as follows:

1. **Run the Postgres Database**:
```bash
docker-compose up -d db pgadmin
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

**Providers**:
- `GET api/v1/providers`: List all providers
- `POST api/v1/providers`: Create a new provider
- `GET api/v1/providers/{id}`: Get details of a provider
- `PUT api/v1/providers/{id}`: Update a provider
- `DELETE /providers/{id}`: Delete a provider

**Service Areas**:
- `GET api/v1/service-areas`: List all service areas
- `POST api/v1/service-areas`: Create a new service area
- `GET api/v1/service-areas/{id}`: Get details of a service area
- `PUT api/v1/service-areas/{id}`: Update a service area
- `DELETE api/v1/service-areas/{id}`: Delete a service area

**Point Geospatial Querying**:
- `GET api/v1/service-areas/search?lat={latitude}&lng={longitude}`: Find service areas containing a specific geo point

## Testing

To test using `curl` commands, you can try creating a Service Area, and check if a latitude/longitude pair is contained in the registered Service Areas:

```bash
curl -X 'POST'   'http://127.0.0.1:8000/api/v1/serviceareas/'   -H 'Content-Type: application/json'   -d '{
  "name": "Downtown Area 2",
  "price": 25.50,
  "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[30.0, 10.0], [40.0, 40.0], [20.0, 40.0], [10.0, 20.0], [30.0, 10.0]]]}"
}'

curl -X GET "http://localhost:8000/api/v1/serviceareas/check?lat=30&lng=20"
```

To run the unit tests:
```bash
pytest
```

## Deployment

<!-- TODO -->
