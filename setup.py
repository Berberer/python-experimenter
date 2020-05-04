from setuptools import setup, find_packages

setup(
    name="python_experimenter",
    version="0.0.1",
    description="Perform and persist custom python experiments.",
    author="Lukas Brandt",
    url="https://github.com/Berberer/python-experimenter",
    packages=find_packages(exclude=("tests", "docs")),
)
