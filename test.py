from python_experimenter.experiment_runner import ExperimentRunner


def calculate_results(keyfields):
    x = int(keyfields["x"])
    y = int(keyfields["y"])
    resultfields = {
        "multiplication": x * y,
        "addition": x + y,
        "substraction": x - y,
        "division": x / y,
    }
    return resultfields


runner = ExperimentRunner(calculate_results, "test.properties")
runner.run()
