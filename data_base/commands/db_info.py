from sqlalchemy.ext.asyncio import create_async_engine
from data_base.structure.models_db import Base


async def create_db(engine: create_async_engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
