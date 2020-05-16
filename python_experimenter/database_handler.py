from abc import ABC, abstractmethod
from python_experimenter.property_handling import required_properties_checker


def create_database_handler_from_config(self, config):
    config_valid = required_properties_checker.check_required_db_properties(
        config
    )
    if config_valid:
        db_type = config["db.type"]
        if db_type == "MYSQL":
            pass  # TODO
        else:
            print(f"Unknown Db type {db_type}. Cannot create DB handler")
    return None


class AbstractDatabaseHandler(ABC):
    def __init__(self):
        super().__init__()

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
    def save_results(self, id, result_fields):
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
