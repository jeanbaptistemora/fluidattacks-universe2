# Standard libraries
import json
from os import environ
from os.path import (
    abspath,
    exists,
    join,
)
from typing import (
    List,
    Tuple,
)

# Third-party libraries
from joblib import load
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC


# Constants
STATIC_DIR: str = environ['SORTS_STATIC_PATH']


def get_extensions_list() -> List[str]:
    """Returns a list with all the extensions allowed"""
    extensions: List[str] = []
    with open(get_static_path('extensions.lst'), 'r') as file:
        extensions = [line.rstrip() for line in file]
    return extensions


def get_static_path(file: str) -> str:
    """Gets the absolute path in both local repository and installed package"""
    static_path: str = abspath(join(STATIC_DIR, file))
    if exists(static_path):
        return static_path
    raise FileNotFoundError(static_path)


def read_allowed_names() -> Tuple[List[str], ...]:
    """Reads static lists containing allowed names and extensions"""
    allowed_names: List[List[str]] = []
    for name in ['extensions.lst', 'composites.lst']:
        with open(get_static_path(name)) as file:
            content_as_list = file.read().split('\n')
            allowed_names.append(list(filter(None, content_as_list)))
    return (allowed_names[0], allowed_names[1])


def load_model() -> MLPClassifier:
    model_path: str = environ['SORTS_MODEL_PATH']
    return load(model_path)


def load_support_vector_machine() -> LinearSVC:
    model = LinearSVC()
    with open(get_static_path('model_parameters.json'), 'r') as mod:
        params = json.load(mod)
    model.coef_ = np.array(params['coef'])
    model.intercept_ = np.array(params['intercept'])
    model.classes_ = np.array(params['classes'])
    return model
