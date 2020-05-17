from python_experimenter.database_handler import (
    create_database_handler_from_config,
    MySqlDatabaseHandler,
)


class TestDatabaseHandlerCreation:
    def test_database_handler_creation(self):
        p = {
            "keyfields": ["x", "y"],
            "resultfields": ["addition", "multiplication"],
            "db.host": ["192.168.0.1"],
            "db.type": ["MYSQL"],
            "db.username": ["experimenter"],
            "db.password": ["1234"],
            "db.database": ["experiments"],
            "db.table": ["test"],
        }
        db_handler = create_database_handler_from_config(p)
        assert db_handler is not None
        assert isinstance(db_handler, MySqlDatabaseHandler)
        assert db_handler.keyfields == ["x", "y"]
        assert db_handler.resultfields == ["addition", "multiplication"]
        assert db_handler.host == "192.168.0.1"
        assert db_handler.user == "experimenter"
        assert db_handler.password == "1234"
        assert db_handler.database == "experiments"
        assert db_handler.table == "test"
        assert not db_handler.is_connected
        assert db_handler.connection is None
        assert db_handler.cursor is None

    def test_unknown_db_type(self):
        p = {
            "keyfields": ["x", "y"],
            "resultfields": ["addition", "multiplication"],
            "db.host": ["192.168.0.1"],
            "db.type": ["DB"],
            "db.username": ["experimenter"],
            "db.password": ["1234"],
            "db.database": ["experiments"],
            "db.table": ["test"],
        }
        db_handler = create_database_handler_from_config(p)
        assert db_handler is None

    def test_invalid_db_config(self):
        p = {
            "keyfields": ["x", "y"],
            "resultfields": ["addition", "multiplication"],
            "db.host": ["192.168.0.1"],
            "db.type": ["DB"],
            "db.username": ["experimenter"],
            "db.password": ["1234"],
            "db.database": ["experiments"],
        }
        db_handler = create_database_handler_from_config(p)
        assert db_handler is None
