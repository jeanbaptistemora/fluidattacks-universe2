# pylint: disable=wrong-import-position
# flake8: noqa E402
"""
We need to manually install sagemaker for training jobs, not tuning ones
If not, we can not import it. Estimator custom dependencies is not
working for sagemaker module.
It installs sagemaker-containers, sagemaker-trainers etc. but not
single sagemaker
"""


import boto3
from sagemaker.tuner import (
    CategoricalParameter,
    IntegerParameter,
)
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
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
        "n_estimators": IntegerParameter(90, 110),
    },
    "adaboostclassifier": {
        "algorithm": CategoricalParameter(["SAMME", "SAMME.R"]),
        "n_estimators": IntegerParameter(40, 60),
    },
}
