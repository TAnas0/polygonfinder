import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.config import settings
from alembic.config import Config
from alembic import command


DATABASE_URL = (
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}@"
    f"{settings.postgres_host}:{settings.postgres_test_port}/{settings.postgres_db}"
)
engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the `get_db` dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply the database override
app.dependency_overrides["get_db"] = override_get_db


ALEMBIC_CONFIG = Config("alembic.ini")


# Alembic migration setup
def run_alembic_migrations():
    ALEMBIC_CONFIG.set_main_option("sqlalchemy.url", DATABASE_URL)
    command.upgrade(ALEMBIC_CONFIG, "head")


# Alembic rollback/downgrade of migrations
def downgrade_all_migrations():
    ALEMBIC_CONFIG.set_main_option("sqlalchemy.url", DATABASE_URL)
    command.downgrade(ALEMBIC_CONFIG, "base")


# Fixture to setup the database for tests.
# Applies Alembic migrations, starts a session for testing, and rollbacks all the changes after each test.
# https://stackoverflow.com/a/67348153/4017403
@pytest.fixture(scope="function")
def setup_db():

    # Run Alembic migrations to set up the database schema
    run_alembic_migrations()

    # Start a session for the test
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        # Rollback any changes made during the test
        db.rollback()
        db.close()

        # Drop all the tables after each test to clean the slate
        downgrade_all_migrations()
