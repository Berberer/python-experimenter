from python_experimenter.property_handling import (
    properties_file_reader,
    required_properties_checker,
    random_property_selector,
)
from python_experimenter.database_handler import (
    create_database_handler_from_config,
)


class ExperimentRunner:
    def __init__(self, evaluation_function, *property_files):
        self.evaluation_function = evaluation_function
        self.properties = {}
        for property_file in property_files:
            self.properties.update(
                properties_file_reader.parse_properties_from_file(
                    property_file
                )
            )

    def run(self):
        if not required_properties_checker.check_experiment_properties(
            self.properties
        ):
            return
        db_handler = create_database_handler_from_config(self.properties)
        if db_handler is None:
            print("Could not create DB handler!")
            return

        if db_handler.is_connected():
            db_handler.check_table_and_create_if_missing(
                self.properties["db.table"]
            )
        else:
            print("Is not connected to DB!")
            return

        experiments_amount = 1
        for keyfield in self.properties["keyfields"]:
            experiments_amount = experiments_amount * len(
                self.properties[keyfield]
            )

        while db_handler.is_connected() and (
            db_handler.count_entries() < experiments_amount
        ):
            experiment_entry = random_property_selector(self.properties)
            experiment_id = db_handler.reserve_entry(experiment_entry)

            if experiment_id is not None:
                try:
                    result_fields = self.evaluation_function(experiment_entry)
                    db_handler.save_results(experiment_id, result_fields)
                except Exception as e:
                    db_handler.save_error(experiment_id, e)
