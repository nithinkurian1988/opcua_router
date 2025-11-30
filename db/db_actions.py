from sqlalchemy.future import select
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
from core.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True, # Use future=True for SQLAlchemy 2.0 style
)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base = declarative_base()

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def init_models():
    '''Initialize database models.'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_all_nodes(model):
    '''Fetch the latest reading of all nodes from table.'''
    async with get_session() as session:
        result = await session.execute(select(model))
        return result.scalars().all()

async def get_node_by_id(model, record_id):
    '''Fetch the latest reading of a node by ID from table.'''
    async with get_session() as session:
        result = await session.execute(
            select(model)
            .where(model.node_id == record_id)
            .order_by(model.id.desc())
        )
        return result.scalars().first()

from db.models import OPCUANode
async def insert_node(node_id: str, value: float):
    new_data = OPCUANode(node_id=node_id, value=value)
    '''Insert a new node into the table.'''
    async with get_session() as session:
        session.add(new_data)
        await session.commit()
        await session.refresh(new_data)
        return new_data

async def delete_node(model, record_id):
    '''Delete complete node record from the table.'''
    async with get_session() as session:
        result = await session.execute(select(model))
        record = result.scalars().all()
        for rec in record:
            if rec.node_id == record_id:
                await session.delete(rec)
                await session.commit()
        return True
    return False
