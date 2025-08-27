# ⚠️ ВНИМАНИЕ: Секреты захардкожены в коде по просьбе владельца.
# Никаких .env и переменных окружения не используется.

from dataclasses import dataclass

@dataclass
class Settings:
    BOT_TOKEN: str = "7961205859:AAEPQvZTdLCzdor-v6h2SAbBaggx_POnpSQ"
    ADMIN_LOGIN: str = "Astra9898"
    ADMIN_PASSWORD: str = "qwert0000123"
    # Можно оставить локальную SQLite рядом с кодом:
    DATABASE_URL: str = "sqlite+aiosqlite:///./data.db"
    # Если хочешь хранить БД вне проекта, поменяй, например:
    # DATABASE_URL: str = "sqlite+aiosqlite:////opt/fieldbot/data/data.db"

settings = Settings()
