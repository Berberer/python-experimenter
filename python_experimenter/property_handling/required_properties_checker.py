def check_required_db_properties(properties):
    if isinstance(properties, dict):
        db_keys = [
            "db.host",
            "db.type",
            "db.username",
            "db.password",
            "db.database",
            "db.table",
        ]
        for key in db_keys:
            if not _has_property_key_with_values(properties, key):
                print(f"{key} is missing in DB properties!")
                return False
        return True
    print("Given properties object is not a dictionary!")
    return False


def check_experiment_properties(properties):
    if isinstance(properties, dict):
        if _has_property_key_with_values(properties, "keyfields"):
            keyfields = properties["keyfields"]
            for keyfield in keyfields:
                if not _has_property_key_with_values(properties, keyfield):
                    msg = keyfield
                    msg = msg + " was declared as a keyfield but is missing!"
                    print(msg)
                    return False
            if _has_property_key_with_values(properties, "resultfields"):
                return True
            else:
                print("resultfields is missing in experiment properties!")
                return False
        else:
            print("keyfields is missing in experiment properties!")
            return False
    print("Given properties object is not a dictionary!")
    return False


def _has_property_key_with_values(properties, key):
    if key in properties:
        values = properties[key]
        return isinstance(values, list) and len(values) > 0
    return False
