from python_experimenter.database_handler import (
    create_database_handler_from_config,
)


class TestMySqlDatabaseHandler:
    def test_mysql_create_table_query_creation(self):
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
        assert db_handler._create_table_query() == (
            "CREATE TABLE test ( "
            "experiment_id int NOT NULL AUTO_INCREMENT, "
            "x varchar(25) NULL, "
            "y varchar(25) NULL, "
            "addition varchar(255) NULL, "
            "multiplication varchar(255) NULL, "
            "start_date datetime NOT NULL, "
            "finished_date datetime NULL, "
            "exception varchar(255) NULL, "
            "PRIMARY KEY (experiment_id), "
            "UNIQUE(x,y) "
            ");"
        )
