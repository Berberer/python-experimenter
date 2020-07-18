import json
import random
import time
import traceback
from python_experimenter.property_handling import (
    properties_file_reader,
    required_properties_checker,
    random_property_selector as selec,
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
        db_handler = None
        try:
            if not required_properties_checker.check_experiment_properties(
                self.properties
            ):
                return
            db_handler = create_database_handler_from_config(self.properties)
            if db_handler is None:
                print("Could not create DB handler!")
                return

            db_handler.open_connection()

            if db_handler.is_connected():
                db_handler.check_table_and_create_if_missing()
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
                experiment_entry = selec.create_random_keyfield_configuration(
                    self.properties
                )
                experiment_id = db_handler.reserve_entry(experiment_entry)

                if experiment_id is not None:
                    try:
                        resultfields = self.evaluation_function(
                            experiment_entry
                        )
                        db_handler.save_results(experiment_id, resultfields)
                    except Exception:
                        db_handler.save_error(
                            experiment_id,
                            json.dumps(
                                traceback.format_exc(chain=False, limit=3)
                            ),
                        )
                time.sleep(random.uniform(1.0, 5.0))

        except Exception:
            print(f"Experiment error: {traceback.format_exc()}")
        finally:
            if db_handler is not None:
                db_handler.close_connection()
