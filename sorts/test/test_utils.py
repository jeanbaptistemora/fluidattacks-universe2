# Standard libraries
import os

# Third party libraries
import csv

# Local libraries
from training.training_script.train import get_best_combination

DATA_PATH: str = f'{os.path.dirname(__file__)}/data'


def test_get_best_combination() -> None:
    expected_results = {
        'best_features': (
            'seldom_contributors',
            'num_lines',
            'commit_frequency'
        ),
        'best_f1': '77'

    }
    with open(
        os.path.join(DATA_PATH, 'test_model_train_results.csv'), 'r'
    ) as csv_file:
        csv_reader = csv.reader(csv_file)
        best_features, best_f1 = get_best_combination(list(csv_reader))
        assert best_features == expected_results['best_features']
        assert best_f1 == expected_results['best_f1']
