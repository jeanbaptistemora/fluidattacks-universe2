from sklearn.ensemble import (
    RandomForestClassifier,
)
from sklearn.neighbors import (
    KNeighborsClassifier,
)
from sklearn.neural_network import (
    MLPClassifier,
)
from sklearn.svm import (
    LinearSVC,
)
from typing import (
    Any,
    Callable,
    Tuple,
    TypeVar,
    Union,
)

Score = Tuple[float, float, float, None]
Model = Union[
    MLPClassifier, RandomForestClassifier, LinearSVC, KNeighborsClassifier
]
Tfun = TypeVar("Tfun", bound=Callable[..., Any])
