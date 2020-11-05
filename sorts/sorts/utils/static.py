# Standard libraries
import json
from os.path import (
    abspath,
    dirname,
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


ROOT: str = abspath(dirname(dirname(dirname(__file__))))


def get_extensions_list() -> List[str]:
    """Returns a list with all the extensions allowed"""
    extensions: List[str] = []
    with open(get_static_path('extensions.lst'), 'r') as file:
        extensions = [line.rstrip() for line in file]
    return extensions


def get_static_path(file: str) -> str:
    """Gets the absolute path in both local repository and installed package"""
    static_file: str = join('static', file)
    for attempt in [
        abspath(join(ROOT, static_file)),
        abspath(join(ROOT, 'site-packages', static_file)),
    ]:
        if exists(attempt):
            return attempt
    raise FileNotFoundError(static_file)


def read_allowed_names() -> Tuple[List[str], ...]:
    """Reads static lists containing allowed names and extensions"""
    allowed_names: List[List[str]] = []
    for name in ['extensions.lst', 'composites.lst']:
        with open(get_static_path(name)) as file:
            content_as_list = file.read().split('\n')
            allowed_names.append(list(filter(None, content_as_list)))
    return (allowed_names[0], allowed_names[1])


def load_neural_network() -> MLPClassifier:
    return load(get_static_path('neural_network.joblib'))


def load_support_vector_machine() -> LinearSVC:
    model = LinearSVC()
    with open(get_static_path('model_parameters.json'), 'r') as mod:
        params = json.load(mod)
    model.coef_ = np.array(params['coef'])
    model.intercept_ = np.array(params['intercept'])
    model.classes_ = np.array(params['classes'])
    return model
