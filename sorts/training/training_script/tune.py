# Standard libraries
import argparse
import os
import tempfile
import time
from typing import (
    Dict,
    List,
    Optional,
    Tuple
)

# Third party Libraries
from pandas import DataFrame

# Local libraries
from sorts.constants import ModelType
from training.constants import FEATURES_DICTS
from training.evaluate_results import get_best_model_name
from training.training_script.utils import (
    get_model_performance_metrics,
    load_training_data,
    split_training_data
)


def get_model_features() -> Tuple[str, ...]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_name_file: str = os.path.join(tmp_dir, 'best_model.txt')
        best_model: str = get_best_model_name(model_name_file)
        inv_features_dict: Dict[str, str] = {
            value: key for key, value in FEATURES_DICTS.items()
        }
        return tuple(
            inv_features_dict[key]
            for key in best_model.upper().split('.')[0].split('-')[2:5]
        )


def train_model(
    model_class: ModelType,
    training_dir: str
) -> List[List[str]]:
    model_features: Tuple[str, ...] = get_model_features()
    start_time: float = time.time()

    training_data: DataFrame = load_training_data(training_dir)
    train_x, train_y = split_training_data(training_data, model_features)

    model = model_class()
    metrics = get_model_performance_metrics(
        model,
        train_x,
        train_y
    )

    print(f'Training time: {time.time() - start_time:.2f}')
    print(f'Features: {model_features}')
    print(f'Precision: {metrics[0]}%')
    print(f'Recall: {metrics[1]}%')
    print(f'F1-Score: {metrics[2]}%')
    print(f'Overfit: {metrics[3]}%')
    training_output = [
        model.__class__.__name__,
        ' '.join(FEATURES_DICTS[feature] for feature in model_features),
        f'{metrics[0]:.1f}',
        f'{metrics[1]:.1f}',
        f'{metrics[2]:.1f}',
        f'{metrics[3]:.1f}'
    ]
    return training_output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output-data-dir',
        type=str,
        default=os.environ['SM_OUTPUT_DATA_DIR']
    )
    parser.add_argument(
        '--model-dir',
        type=str,
        default=os.environ['SM_MODEL_DIR']
    )
    parser.add_argument(
        '--train',
        type=str,
        default=os.environ['SM_CHANNEL_TRAIN']
    )
    parser.add_argument('--model', type=str, default='')
    parser.add_argument('--activation', type=str, default='')
    args = parser.parse_args()

    model: str = args.model
    model_class: Optional[ModelType] = globals().get(model)
    _ = train_model(
        model_class,
        args.train
    )


if __name__ == '__main__':
    main()
