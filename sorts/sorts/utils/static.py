# Standard libraries
import os
from typing import (
    List,
    Tuple,
)

# Third-party libraries
from joblib import load
from sklearn.neural_network import MLPClassifier


STATIC_PATH: str = f'{os.path.dirname(__file__)}/../static'


def read_allowed_names() -> Tuple[List[str], ...]:
    """Reads static lists containing allowed names and extensions"""
    allowed_names: List[List[str]] = []
    for name in ['extensions.lst', 'composites.lst']:
        with open(os.path.join(STATIC_PATH, name)) as file:
            content_as_list = file.read().split('\n')
            allowed_names.append(list(filter(None, content_as_list)))
    return (allowed_names[0], allowed_names[1])


def load_neural_network() -> MLPClassifier:
    return load(os.path.join(STATIC_PATH, 'neural_network.joblib'))
