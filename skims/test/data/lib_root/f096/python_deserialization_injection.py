# pylint: skip-file
import pickle
from test.yaml import (
    yaml,
)
from typing import (
    Any,
)


def unsafe_loads(request: Any) -> None:
    file_to_load = request.files["pickle"]
    # Noncompliant: Using pickle module to deserialize user inputs
    pickle.load(file_to_load)
    data = request.GET.get("data")
    # Noncompliant: Using yaml.load with unsafe yaml.Loader
    yaml.load(data, Loader=yaml.Loader)


def safe_loads(request: Any, some_data: Any) -> None:
    data = request.GET.get("data")
    # Compliant:  Using yaml.load with the default safe loader
    yaml.load(data)
    # Non-deterministic: The data is not a user param
    yaml.load(some_data, Loader=yaml.Loader)
    pickle.load(some_data)
