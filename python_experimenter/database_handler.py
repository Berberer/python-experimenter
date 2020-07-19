import mysql.connector
from abc import ABC, abstractmethod
from python_experimenter.property_handling import required_properties_checker


def create_database_handler_from_config(config):
    config_valid = required_properties_checker.check_required_db_properties(
        config
    )
    if config_valid:
        db_type = config["db.type"][0]
        db_host = config["db.host"][0]
        db_user = config["db.username"][0]
        db_password = config["db.password"][0]
        db_database = config["db.database"][0]
        db_table = config["db.table"][0]
        keyfields = config["keyfields"]
        resultfields = config["resultfields"]
        if db_type == "MYSQL":
            return MySqlDatabaseHandler(
                db_host,
                db_user,
                db_password,
                db_database,
                db_table,
                keyfields,
                resultfields,
            )
        else:
            print(f"Unknown Db type {db_type}. Cannot create DB handler")
    return None


class AbstractDatabaseHandler(ABC):
    def __init__(
        self, host, user, password, database, table, keyfields, resultfields
    ):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.keyfields = keyfields
        self.resultfields = resultfields
        self.connected = False
        self.connection = None
        self.cursor = None

    @abstractmethod
    def open_connection(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def check_table_and_create_if_missing(self):
        pass

    @abstractmethod
    def reserve_entry(self, entry):
        pass

    @abstractmethod
    def save_results(self, id, resultfields):
        pass

    @abstractmethod
    def save_error(self, id, error):
        pass

    @abstractmethod
    def count_entries(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass


class MySqlDatabaseHandler(AbstractDatabaseHandler):
    def open_connection(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database,
            )
            self.cursor = self.connection.cursor()
            self.connected = True
        except Exception as e:
            print(f"Error during MySQL connect: {e}")

    def is_connected(self):
        if self.connection is None:
            return False

        if self.connected:
            try:
                self.connected = self.connection.is_connected()
            except Exception as e:
                print(f"Error during MySQL connection check: {e}")

        if not self.connected:
            try:
                self.connection.reconnect(attempts=3, delay=5)
                self.connected = self.connection.is_connected()
                if self.connected:
                    try:
                        if self.cursor is not None:
                            self.cursor.close()
                    finally:
                        self.cursor = self.connection.cursor()
            except Exception as e:
                print(f"Error during MySQL reconnect: {e}")

        return self.connected

    def check_table_and_create_if_missing(self):
        if self._can_execute():
            table_check = (
                f"SELECT * "
                f"FROM information_schema.tables "
                f"WHERE table_schema = '{self.database}' "
                f"AND table_name = '{self.table}' "
                f"LIMIT 1;"
            )
            table_exists = False
            try:
                self.cursor.execute(table_check)
                result = self.cursor.fetchall()
                if result is not None and len(result) == 1:
                    table_exists = True
            except Exception as e:
                print(f"Error during MySQL table exists check: {e}")

            if not table_exists:
                try:
                    self.cursor.execute(self._create_table_query())
                except Exception as e:
                    print(f"Error during MySQL table creation: {e}")

    def reserve_entry(self, entry):
        if self._can_execute():
            check_query = f"SELECT COUNT(*) FROM {self.table} WHERE "
            keyfield_comparisons = list(
                map(lambda k: f"{k} = '{entry[k]}'", self.keyfields)
            )
            check_query = check_query + " AND ".join(keyfield_comparisons)
            check_query = check_query + ";"
            self.cursor.execute(check_query)

            if self.cursor.fetchone()[0] == 0:
                keyfield_values = ",".join(
                    list(map(lambda k: f"'{entry[k]}'", self.keyfields))
                )
                reserve_query = (
                    f"INSERT INTO {self.table} "
                    f"({','.join(self.keyfields)},start_date) "
                    f"VALUES ({keyfield_values},NOW());"
                )
                self.cursor.execute(reserve_query)
                self.connection.commit()
                return self.cursor.lastrowid

        return None

    def save_results(self, id, resultfields):
        if self._can_execute():
            resultfield_values = []
            for resultfield in self.resultfields:
                if resultfield in resultfields:
                    resultfield_values.append(
                        f"{resultfield} = {resultfields[resultfield]}"
                    )
            query = (
                f"UPDATE {self.table} "
                f"SET finished_date = NOW(), "
                f"{','.join(resultfield_values)} "
                f"WHERE experiment_id = {id};"
            )
            self.cursor.execute(query)
            self.connection.commit()

    def save_error(self, id, error):
        if self._can_execute():
            query = (
                f"UPDATE {self.table} "
                f"SET finished_date = NOW(), exception = '{error}' "
                f"WHERE experiment_id = {id};"
            )
            self.cursor.execute(query)
            self.connection.commit()

    def count_entries(self):
        result = 0
        if self._can_execute():
            try:
                self.cursor.execute(f"SELECT COUNT(*) FROM {self.table};")
                result = self.cursor.fetchone()[0]
            except Exception as e:
                print(f"Error during MySQL row count: {e}")
        return result

    def close_connection(self):
        if self.connection is not None and self.connected:
            try:
                if self.cursor is not None:
                    self.cursor.close()
                self.connection.close()
            except Exception as e:
                print(f"Error during closing MySQL connection : {e}")

    def _can_execute(self):
        return self.connected and self.cursor is not None

    def _create_table_query(self):
        query = (
            f"CREATE TABLE {self.table} ( "
            f"experiment_id int NOT NULL AUTO_INCREMENT, "
        )

        for keyfield in self.keyfields:
            query = query + (f"{keyfield} varchar(25) NULL, ")

        for resultfield in self.resultfields:
            query = query + (f"{resultfield} varchar(255) NULL, ")

        query = query + (
            f"start_date datetime NOT NULL, "
            f"finished_date datetime NULL, "
            f"exception text NULL, "
            f"PRIMARY KEY (experiment_id), "
            f"UNIQUE({','.join(self.keyfields)}) "
            f");"
        )

        return query
