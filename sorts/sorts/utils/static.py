from joblib import (
    load,
)
import json
import numpy as np
from os import (
    environ,
)
from os.path import (
    abspath,
    exists,
    join,
)
from sklearn.neural_network import (
    MLPClassifier,
)
from sklearn.svm import (
    LinearSVC,
)
from sorts.constants import (
    STATIC_DIR,
)
from typing import (
    List,
    Tuple,
)


def get_extensions_list() -> List[str]:
    """Returns a list with all the extensions allowed"""
    extensions: List[str] = []
    with open(get_static_path("extensions.lst"), "r", encoding="utf8") as file:
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
    for name in ["extensions.lst", "composites.lst"]:
        with open(get_static_path(name), encoding="utf8") as file:
            content_as_list = file.read().split("\n")
            allowed_names.append(list(filter(None, content_as_list)))

    return (allowed_names[0], allowed_names[1])


def load_model() -> MLPClassifier:
    model_path: str = environ["SORTS_MODEL_PATH"]

    return load(model_path)


def load_support_vector_machine() -> LinearSVC:
    model = LinearSVC()
    with open(
        get_static_path("model_parameters.json"), "r", encoding="utf8"
    ) as mod:
        params = json.load(mod)
    model.coef_ = np.array(params["coef"])
    model.intercept_ = np.array(params["intercept"])
    model.classes_ = np.array(params["classes"])

    return model
