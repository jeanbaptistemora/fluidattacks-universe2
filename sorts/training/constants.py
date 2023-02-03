import boto3
from lightgbm import (
    LGBMClassifier,
)
from sagemaker.tuner import (
    CategoricalParameter,
    ContinuousParameter,
    IntegerParameter,
)
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import (
    LogisticRegression,
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
    Union,
)
from xgboost import (
    XGBClassifier,
)

# Threshold defining the minimum elements that our dataset must have (*1000)
DATASET_THRESHOLD: int = 40

# AWS-related
S3_BUCKET_NAME: str = "sorts"
S3_RESOURCE = boto3.resource("s3")
S3_BUCKET = S3_RESOURCE.Bucket(S3_BUCKET_NAME)

DATASET_PATH: str = "s3://sorts/training/binary_encoded_training_data.csv"

SAGEMAKER_METRIC_DEFINITIONS: List[Dict[str, str]] = [
    {"Name": "precision", "Regex": "Precision: (.*?)%"},
    {"Name": "recall", "Regex": "Recall: (.*?)%"},
    {"Name": "fscore", "Regex": "F1-Score: (.*?)%"},
    {"Name": "accuracy", "Regex": "Accuracy: (.*?)%"},
    {"Name": "overfit", "Regex": "Overfit: (.*?)%"},
]

# Model-related
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
    "Accuracy",
    "Overfit",
    "TunedParams",
    "Time",
]
MODELS: Dict[str, ModelType] = {
    "adaboostclassifier": AdaBoostClassifier,
    "gradientboostingclassifier": GradientBoostingClassifier,
    "histgradientboostingclassifier": HistGradientBoostingClassifier,
    "kneighborsclassifier": KNeighborsClassifier,
    "lgbmclassifier": LGBMClassifier,
    "linearsvc": LinearSVC,
    "logisticregression": LogisticRegression,
    "mlpclassifier": MLPClassifier,
    "randomforestclassifier": RandomForestClassifier,
    "xgbclassifier": XGBClassifier,
}
MODELS_DEFAULTS: Dict[ModelType, Dict[str, Union[str, int, float]]] = {
    LGBMClassifier: {
        "learning_rate": 0.05,
        "max_depth": 3,
    },
    LinearSVC: {"dual": False},
    LogisticRegression: {"max_iter": 2000},
    MLPClassifier: {"max_iter": 500},
    XGBClassifier: {
        "learning_rate": 0.01,
        "max_depth": 4,
        "min_child_weight": 6,
        "subsample": 0.5,
    },
}

# Hyperparameters
MODEL_HYPERPARAMETERS = {
    "adaboostclassifier": {
        "algorithm": CategoricalParameter(["SAMME", "SAMME.R"]),
        "n_estimators": IntegerParameter(40, 60),
    },
    "gradientboostingclassifier": {
        "n_estimators": IntegerParameter(105, 115),
        "learning_rate": ContinuousParameter(
            0.01, 0.06, scaling_type="Logarithmic"
        ),
    },
    "histgradientboostingclassifier": {
        "max_leaf_nodes": CategoricalParameter([0, 5, 25, 50, 100, 250, 500]),
        "learning_rate": ContinuousParameter(
            0.1, 1, scaling_type="Logarithmic"
        ),
    },
    "kneighborsclassifier": {
        "algorithm": CategoricalParameter(
            ["auto", "ball_tree", "kd_tree", "brute"]
        ),
        "n_neighbors": IntegerParameter(4, 9),
    },
    "lgbmclassifier": {
        "max_depth": IntegerParameter(3, 6),
        "learning_rate": ContinuousParameter(
            0.01, 0.08, scaling_type="Logarithmic"
        ),
    },
    "linearsvc": {
        "loss": CategoricalParameter(["hinge", "squared_hinge"]),
        "multi_class": CategoricalParameter(["ovr", "crammer_singer"]),
    },
    "logisticregression": {
        "solver": CategoricalParameter(
            ["lbfgs", "sag", "saga", "liblinear", "newton-cg"]
        ),
    },
    "mlpclassifier": {
        "activation": CategoricalParameter(
            ["relu", "tanh", "identity", "logistic"]
        ),
        "solver": CategoricalParameter(["lbfgs", "sgd", "adam"]),
    },
    "randomforestclassifier": {
        "n_estimators": IntegerParameter(40, 60),
        "max_depth": IntegerParameter(3, 6),
    },
    "xgbclassifier": {
        "learning_rate": ContinuousParameter(
            0.01, 0.07, scaling_type="Logarithmic"
        ),
        "max_depth": IntegerParameter(3, 5),
        "min_child_weight": IntegerParameter(3, 6),
    },
}
