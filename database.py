from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv  
import os

load_dotenv()

URL_DATABASE = os.getenv('DATABASE_URL')

engine = create_async_engine(URL_DATABASE,connect_args={"check_same_thread": False})
Base = declarative_base()
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session