# Standard libraries
from typing import (
    Dict,
    List
)

# Third party libraries
import boto3
from sagemaker.tuner import CategoricalParameter
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC

# Local libraries
from sorts.typings import Model as ModelType


S3_BUCKET_NAME: str = 'sorts'
S3_RESOURCE = boto3.resource('s3')
S3_BUCKET = S3_RESOURCE.Bucket(S3_BUCKET_NAME)

FEATURES_DICTS: Dict[str, str] = {
    'num_commits': 'CM',
    'num_unique_authors': 'AU',
    'file_age': 'FA',
    'midnight_commits': 'MC',
    'risky_commits': 'RC',
    'seldom_contributors': 'SC',
    'num_lines': 'LC',
    'busy_file': 'BF',
    'commit_frequency': 'CF'
}
RESULT_HEADERS: List[str] = [
    'Model',
    'Features',
    'Precision',
    'Recall',
    'F1',
    'Overfit'
]
MODELS: Dict[str, ModelType] = {
    'mlpclassifier': MLPClassifier,
    'randomforestclassifier': RandomForestClassifier,
    'kneighborsclassifier': KNeighborsClassifier,
    'linearsvc': LinearSVC,
    'gradientboostingclassifier': GradientBoostingClassifier
}

# Hyperparameters
MODEL_HYPERPARAMETERS = {
    'mlpclassifier': {
        'activation': CategoricalParameter([
            'relu',
            'tanh',
            'identity',
            'logistic'
        ]),
        'solver': CategoricalParameter([
            'lbfgs',
            'sgd',
            'adam'
        ]),
    },
}
