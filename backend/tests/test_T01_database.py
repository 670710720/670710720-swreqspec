from importlib import import_module

from app.db.models import Base


def test_T01_creates_required_tables_without_national_id(
    database_engine, database_inspector
):
    migration = import_module("app.db.migrations.001_init")
    Base.metadata.drop_all(database_engine)
    migration.upgrade(database_engine)

    assert {"slots", "bookings", "audit_logs"} <= set(
        database_inspector.get_table_names()
    )
    assert "national_id" not in {
        column["name"] for column in database_inspector.get_columns("bookings")
    }
    assert callable(migration.upgrade)
