from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from src.database import DATABASE_URL
from src.models import Base


from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# Set the URL in the Alembic config
config.set_main_option('sqlalchemy.url', DATABASE_URL)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
target_metadata = Base.metadata
# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# Configure Alembic to ignore PostGIS-related tables
POSTGIS_TABLES = [
    "spatial_ref_sys",
    "geometry_columns",
    "geography_columns",
    "raster_columns",
    "raster_overviews",
    "topology",
    "layer",
    "topology_id_seq",
    'loader_lookuptables',
    'pagc_rules',
    'zip_state',
    'secondary_unit_lookup',
    'geocode_settings_default',
    'place',
    'loader_platform',
    'zip_lookup',
    'county',
    'featnames',
    'direction_lookup',
    'cousub',
    'edges',
    'loader_variables',
    'addrfeat',
    'county_lookup',
    'bg',
    'addr',
    'geocode_settings',
    'faces',
    'countysub_lookup',
    'zip_lookup_all',
    'pagc_gaz',
    'state_lookup',
    'tabblock20',
    'zcta5',
    'tract',
    'pagc_lex',
    'street_type_lookup',
    'state',
    'place_lookup',
    'zip_state_loc',
    'zip_lookup_base',
    'tabblock',
]


def include_object(object, name, type_, reflected, compare_to):
    """Should this table be managed by alembic or not?"""
    if type_ == "table" and name in POSTGIS_TABLES:  # Add other PostGIS tables here if necessary
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
