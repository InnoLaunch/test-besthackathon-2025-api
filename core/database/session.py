from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from server.config import config
from core.database.jsonencoder import custom_serializer

engine = create_async_engine(config.DB_URL, json_serializer=custom_serializer)

Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    """
    Get the database session.
    This can be used for dependency injection.

    :return: The database session.
    """
    session = Session()
    try:
        yield session
    except Exception as exc:
        await session.rollback()
        raise exc
    finally:
        await session.close()
