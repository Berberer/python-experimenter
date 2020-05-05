import python_experimenter.property_handling.random_property_selector as s


class TestRandomKeyFieldSelection:
    def test_random_keyfield_selection(self):
        properties = {
            "keyfields": ["x", "y", "z"],
            "a": [1, 2, 3],
            "b": ["test", "abc"],
            "x": ["x", "y", "z"],
            "y": [42, 43, 44],
            "z": ["abc", "def", "ghi", "jkl"],
        }
        configuration = s.create_random_keyfield_configuration(properties)
        assert len(configuration) == 3
        assert "x" in configuration
        assert configuration["x"] in properties["x"]
        assert "y" in configuration
        assert configuration["y"] in properties["y"]
        assert "z" in configuration
        assert configuration["z"] in properties["z"]
