import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from app.db.models import Base


@pytest.fixture
def database_engine():
    """เตรียมฐานข้อมูล SQLite ในหน่วยความจำสำหรับการทดสอบโมเดล"""
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def database_session(database_engine):
    """เปิด session สำหรับการทดสอบฐานข้อมูล"""
    with Session(database_engine) as session:
        yield session


@pytest.fixture
def database_inspector(database_engine):
    """ตรวจ schema ที่ migration สร้างขึ้น"""
    return inspect(database_engine)
