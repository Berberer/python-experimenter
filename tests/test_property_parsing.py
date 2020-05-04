import python_experimenter.property_parsing.properties_file_reader as r
import python_experimenter.property_parsing.required_properties_checker as c


class TestPropertyFileHandling:
    def test_parsing_of_correct_file(self):
        p = r.parse_properties_from_file(
            "res/test_property_files/correct.properties"
        )
        assert p == {
            "keyfields": ["x", "y"],
            "resultfields": ["addition", "multiplication"],
            "x": ["1", "2", "3"],
            "y": ["4", "5", "6"],
            "db.host": ["192.168.0.1"],
            "db.username": ["experimenter"],
            "db.password": ["1234"],
            "db.database": ["experiments"],
            "db.table": ["test"],
        }

    def test_correct_property_checking(self):
        p = r.parse_properties_from_file(
            "res/test_property_files/correct.properties"
        )
        assert c.check_required_db_properties(p)
        assert c.check_experiment_properties(p)

    def test_incorrect_db_check(self):
        incorrect_files = [
            "res/test_property_files/db_prop_empty.properties",
            "res/test_property_files/db_prop_missing.properties",
        ]
        for f in incorrect_files:
            p = r.parse_properties_from_file(f)
            assert not c.check_required_db_properties(p)
            assert c.check_experiment_properties(p)

    def test_incorrect_experiment_check(self):
        incorrect_files = [
            "res/test_property_files/keyfield_value_empty.properties",
            "res/test_property_files/keyfield_value_missing.properties",
            "res/test_property_files/keyfields_empty.properties",
            "res/test_property_files/keyfields_missing.properties",
            "res/test_property_files/resultfields_empty.properties",
            "res/test_property_files/resultfields_missing.properties",
        ]
        for f in incorrect_files:
            p = r.parse_properties_from_file(f)
            assert not c.check_experiment_properties(p)
            assert c.check_required_db_properties(p)

    def test_non_dict_input(self):
        assert not c.check_experiment_properties(123)
        assert not c.check_required_db_properties(123)
