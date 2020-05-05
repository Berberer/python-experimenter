import random


def create_random_keyfield_configuration(properties):
    configuration = {}
    keyfields = properties["keyfields"]
    for keyfield in keyfields:
        configuration[keyfield] = random.choice(properties[keyfield])
    return configuration
