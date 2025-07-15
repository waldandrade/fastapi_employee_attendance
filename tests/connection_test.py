import pytest
from app import models
from app.infra.db.settings.connections import DBConnectionHandler
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

@pytest.mark.skip(reason="Teste sensível")
def test_create_database_engine():
    db_connection_handle = DBConnectionHandler()
    engine = db_connection_handle.get_engine()
    assert engine is not None