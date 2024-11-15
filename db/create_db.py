# db/create_db.py

import logging
from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка логирования
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)  # Уровень ERROR

# Настройки базы данных
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Определяем базу данных
Base = declarative_base()

# Определяем модель пользователя
class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True, index=True)  # ID пользователя в Telegram
    has_access = Column(Boolean, default=False)  # Доступ (по умолчанию False)
    sent_messages_count = Column(Integer, default=0)  # Количество отправленных сообщений (по умолчанию 0)

# Создаем асинхронный движок и сессию
engine = create_async_engine(DATABASE_URL, echo=False)  # Установите echo=False
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)

async def create_user(telegram_id: int, has_access: bool = False):
    async with AsyncSessionLocal() as session:
        new_user = User(telegram_id=telegram_id, has_access=has_access)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

async def update_access(telegram_id: int, has_access: bool):
    async with AsyncSessionLocal() as session:
        # Находим пользователя по telegram_id
        user = await session.get(User, telegram_id)
        if user:
            user.has_access = has_access  # Обновляем доступ
            await session.commit()  # Сохраняем изменения
            await session.refresh(user)  # Обновляем объект пользователя
            return user
        else:
            return None  # Если пользователь не найден
        

async def get_user_by_telegram_id(telegram_id: int):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, telegram_id)  # Получаем пользователя по telegram_id
        return user  # Возвращаем пользователя или None, если не найден