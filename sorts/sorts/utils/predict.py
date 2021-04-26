# Standard libraries
from typing import List

# Third-party libraries
import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame
from prettytable import (
    from_csv,
    PrettyTable,
)

# Local libraries
from sorts.typings import Model as ModelType
from sorts.utils.logs import log
from sorts.utils.static import (
    load_model,
    load_support_vector_machine,
)


def get_scope_from_csv_name(csv_name: str) -> str:
    return csv_name.split('.')[0].split('_')[-1]


def build_results_csv(
    predictions: ndarray,
    predict_df: DataFrame,
    csv_name: str
) -> None:
    scope: str = get_scope_from_csv_name(csv_name)
    result_df: DataFrame = pd.concat(
        [
            predict_df[[scope]],
            pd.DataFrame(
                predictions,
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
    sorted_files.to_csv(csv_name, index=False)

    log(
        'info',
        'Results saved to file %s.',
        csv_name
    )


def display_results(csv_name: str) -> None:
    scope: str = get_scope_from_csv_name(csv_name)
    log(
        'info',
        'Here are the top 20 files to check:'
    )
    with open(csv_name, 'r') as csv_file:
        table: PrettyTable = from_csv(
            csv_file,
            field_names=[scope, 'prob_vuln'],
            delimiter=','
        )
    table.align[scope] = 'l'
    # pylint: disable=protected-access
    table._max_width = {scope: 120, 'prob_vuln': 10}

    print(table.get_string(start=1, end=20))


def predict_vuln_prob(
    predict_df: DataFrame,
    features: List[str],
    csv_name: str,
    scope: str
) -> None:
    """Uses model to make predictions on the input and save them to CSV"""
    if scope == 'file':
        model: ModelType = load_model()
        input_data = predict_df[model.feature_names + features]
        probability_prediction: ndarray = model.predict_proba(input_data)
    elif scope == 'commit':
        input_data = predict_df[features]
        model = load_support_vector_machine()
        # pylint: disable=protected-access
        probability_prediction = model._predict_proba_lr(input_data)
    class_prediction: ndarray = model.predict(input_data)
    merged_predictions: ndarray = np.column_stack([
        class_prediction,
        probability_prediction
    ])

    build_results_csv(
        merged_predictions,
        predict_df,
        csv_name
    )
