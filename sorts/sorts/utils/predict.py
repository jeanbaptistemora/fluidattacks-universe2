# Standard libraries
from typing import (
    List,
    Union,
)

# Third-party libraries
import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC

# Local libraries
from utils.logs import log
from utils.static import (
    load_neural_network,
    load_support_vector_machine,
)


Model = Union[LinearSVC, MLPClassifier]


def predict_vuln_prob(
    predict_df: DataFrame,
    features: List[str],
    group: str,
    scope: str
) -> None:
    """Uses model to make predictions on the input and save them to CSV"""
    input_data: DataFrame = predict_df[features]
    if scope == 'file':
        model: Model = load_neural_network()
        probability_prediction: ndarray = model.predict_proba(input_data)
    elif scope == 'commit':
        model = load_support_vector_machine()
        # pylint: disable=protected-access
        probability_prediction = model._predict_proba_lr(input_data)
    class_prediction: ndarray = model.predict(input_data)
    merged_predictions: ndarray = np.column_stack([
        class_prediction,
        probability_prediction
    ])
    result_df: DataFrame = pd.concat(
        [
            predict_df[[scope]],
            pd.DataFrame(
                merged_predictions,
                columns=['pred', 'prob_safe', 'prob_vuln']
            )
        ],
        axis=1
    )
    errort: float = 5 + 5 * np.random.rand(len(result_df), )
    result_df['prob_vuln'] = round(result_df.prob_vuln * 100 - errort, 1)
    sorted_files: DataFrame = result_df[result_df.pred == 1]\
        .sort_values(by='prob_vuln', ascending=False)\
        .reset_index(drop=True)[[scope, 'prob_vuln']]
    csv_name: str = f'{group}_sorts_results_{scope}.csv'
    sorted_files.to_csv(csv_name, index=False)
    log('info', 'Results saved to file %s', csv_name)
