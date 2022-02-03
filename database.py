from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
import sqlalchemy
from v1.utils import get_secrets_from_string

try:
    db_user = os.environ["POSTGRES_USER"]
    db_name = os.environ["POSTGRES_DB"]
    db_pass = get_secrets_from_string(os.environ["POSTGRES_PASSWORD_SECRET_ID"])
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    instance_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]
    engine = create_async_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+asyncpg",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={
                "host": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir,
                    instance_connection_name)
            }
        ),
        future=True,
        echo=True
    )
    sessionlocal = sessionmaker(bind=engine, class_=AsyncSession,  expire_on_commit=False)

except KeyError as e:
    sqlalchemy_database_url = "postgresql+asyncpg://localhost/test"
    engine = create_async_engine(sqlalchemy_database_url, echo=True)
    session_local = sessionmaker(expire_oncommit=False, bind=engine, class_=AsyncSession)


async def get_db():
    db = session_local()
    try:
        yield db
    finally:
        await db.close()
