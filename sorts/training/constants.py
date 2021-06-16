import boto3
from sagemaker.tuner import (
    CategoricalParameter,
    ContinuousParameter,
    IntegerParameter,
)

from sklearn.experimental import (  # noqa  # isort: split
    enable_hist_gradient_boosting,
)
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
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
from sorts.typings import (
    Model as ModelType,
)
from typing import (
    Dict,
    List,
)

S3_BUCKET_NAME: str = "sorts"
S3_RESOURCE = boto3.resource("s3")
S3_BUCKET = S3_RESOURCE.Bucket(S3_BUCKET_NAME)

FEATURES_DICTS: Dict[str, str] = {
    "num_commits": "CM",
    "num_unique_authors": "AU",
    "file_age": "FA",
    "midnight_commits": "MC",
    "risky_commits": "RC",
    "seldom_contributors": "SC",
    "num_lines": "LC",
    "busy_file": "BF",
    "commit_frequency": "CF",
}
RESULT_HEADERS: List[str] = [
    "Model",
    "Features",
    "Precision",
    "Recall",
    "F1",
    "Overfit",
]
MODELS: Dict[str, ModelType] = {
    "adaboostclassifier": AdaBoostClassifier,
    "gradientboostingclassifier": GradientBoostingClassifier,
    "histgradientboostingclassifier": HistGradientBoostingClassifier,
    "kneighborsclassifier": KNeighborsClassifier,
    "linearsvc": LinearSVC,
    "mlpclassifier": MLPClassifier,
    "randomforestclassifier": RandomForestClassifier,
}

# Hyperparameters
MODEL_HYPERPARAMETERS = {
    "mlpclassifier": {
        "activation": CategoricalParameter(
            ["relu", "tanh", "identity", "logistic"]
        ),
        "solver": CategoricalParameter(["lbfgs", "sgd", "adam"]),
    },
    "gradientboostingclassifier": {
        "criterion": CategoricalParameter(["friedman_mse", "mse", "mae"]),
        "loss": CategoricalParameter(["deviance", "exponential"]),
        "max_depth": IntegerParameter(3, 5),
        "n_estimators": IntegerParameter(105, 115),
        "learning_rate": ContinuousParameter(0.03, 0.1),
    },
    "adaboostclassifier": {
        "algorithm": CategoricalParameter(["SAMME", "SAMME.R"]),
        "n_estimators": IntegerParameter(40, 60),
    },
}
