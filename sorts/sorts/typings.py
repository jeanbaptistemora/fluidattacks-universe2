# Standard libraries
from typing import (
    Tuple,
    Union
)

# Third party libraries
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC


Score = Tuple[float, float, float, None]
Model = Union[
    MLPClassifier,
    RandomForestClassifier,
    LinearSVC,
    KNeighborsClassifier
]
