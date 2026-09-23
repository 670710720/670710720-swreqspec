import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_database_url() -> str:
    """อ่าน URL ฐานข้อมูลตาม CON-TECH-01 โดยไม่ฝังค่า credential ในโค้ด"""
    return os.getenv("DATABASE_URL", "postgresql+psycopg://localhost/booking")


def create_database_engine(database_url: str | None = None):
    """สร้าง engine สำหรับ PostgreSQL จริงหรือฐานข้อมูลทดสอบตาม CON-TECH-01"""
    return create_engine(database_url or get_database_url(), future=True)


engine = create_database_engine()
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
