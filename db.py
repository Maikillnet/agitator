from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from .config import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    from . import models  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    await _ensure_schema()

async def _ensure_schema():
    """Мягкие миграции для SQLite: добавляем недостающие колонки в agent."""
    async with engine.begin() as conn:
        res = await conn.execute(text("PRAGMA table_info(agent)"))
        cols = [row[1] for row in res]
        if "admin_logged_in" not in cols:
            try:
                await conn.execute(text("ALTER TABLE agent ADD COLUMN admin_logged_in BOOLEAN DEFAULT 0"))
            except Exception:
                pass
        if "username" not in cols:
            try:
                await conn.execute(text("ALTER TABLE agent ADD COLUMN username VARCHAR(255)"))
            except Exception:
                pass
