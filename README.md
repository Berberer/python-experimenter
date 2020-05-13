# Python Experimenter
Construct and manage experiments written in Python managed with a database and configured with a simple `.properties` file.

With the database as a single control instance it is particularly suited for running the experiments as multiple distributed instances.

This experiment runner is adopted and ported to Python from the Java [AILibs experiments package](https://github.com/fmohr/AILibs/tree/master/JAICore/jaicore-experiments).

## Configuration
A properties file for a simple mathematic operations experiment could look for example like the following:
```
db.host = 192.168.0.1
db.type = MYSQL
db.username = experimenter
db.password = 123
db.database = experiments
db.table = test

keyfields=x,y
resultfields=multiplication,addition
x=1,2,3
y=4,5,6
```
With such a configuration the experimenter would connect to the `experiments` database, check if the `test` table exists, and create if otherwise.

Currently only `MYSQL` is supported for `db.type`, but other types can easily be integrated by extending `python_experimenter/database_handler.py`.

After checking for an existing table and possibly creating a new one, it looks up in the table which combinations of the key-fields x and y are not created yet and reserve the missing combination for this instance.
For example, if the combination x=2 and y=4 is missing from the table, it will call the custom experiment function and persist the computed result-fields in a new database row.

Such a custom experiment function for the multiplication and addition example could look like this:
```python
def calculate_results(keyfields):
    x = keyfields["x"]
    y = keyfields["y"]
    resultfields = {
        "multiplication": x * y,
        "addition": x + y
    }
    return resultfields
```
This function will be called iteratively with random combinations not included in the table, until each possible combination is present.

The complete experiment can be run with the following snippet for the example:
```python
from python_experimenter.experiment_runner import ExperimentRunner

runner = ExperimentRunner(calculate_results, <path to properties file>)
runner.run()
```
