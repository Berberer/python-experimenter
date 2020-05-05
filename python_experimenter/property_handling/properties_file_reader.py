def parse_properties_from_file(path):
    parsed_properties = {}
    with open(path, "r") as property_file:
        properties = property_file.readlines()
        for prop in properties:
            line = prop.strip().split("#")
            line = line[0].strip()
            if len(line) > 0 and line[0] != "#":
                assignment = line.split("=")
                key = assignment[0].strip()
                value = assignment[1].strip()
                parsed_value = [value]
                if "," in value:
                    parsed_value = list(
                        map(lambda a: a.strip(), value.split(","))
                    )
                parsed_properties[key] = list(
                    filter(lambda a: len(a) > 0, parsed_value)
                )
    return parsed_properties
