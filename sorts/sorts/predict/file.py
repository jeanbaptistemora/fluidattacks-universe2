# Standard libraries
import os
from typing import List

# Third-party libraries
import pandas as pd
from pandas import DataFrame

# Local libraries
from sorts.features.file import extract_features
from sorts.utils.logs import log
from sorts.utils.predict import predict_vuln_prob
from sorts.utils.repositories import get_repository_files
from sorts.utils.static import (
    get_extensions_list,
    read_allowed_names,
)


def get_subscription_files_df(fusion_path: str) -> DataFrame:
    """Builds the basic DF with all the files from every repository"""
    files: List[str] = []
    extensions, composites = read_allowed_names()
    for repo in os.listdir(fusion_path):
        repo_files = get_repository_files(os.path.join(fusion_path, repo))
        allowed_files = list(
            filter(
                lambda x: (
                    x in composites or
                    x.split('.')[-1].lower() in extensions
                ),
                repo_files
            )
        )
        if allowed_files:
            files.extend(allowed_files)
    files_df: DataFrame = pd.DataFrame(files, columns=['file'])
    files_df['repo'] = files_df['file'].apply(
        lambda x: os.path.join(fusion_path, x.split('/')[0])
    )
    return files_df


def prioritize(subscription_path: str) -> bool:
    """Prioritizes files according to the chance of finding a vulnerability"""
    success: bool = False
    group: str = os.path.basename(os.path.normpath(subscription_path))
    fusion_path: str = os.path.join(subscription_path, 'fusion')
    if os.path.exists(fusion_path):
        predict_df: DataFrame = get_subscription_files_df(fusion_path)
        success = extract_features(predict_df)
        if success:
            extensions: List[str] = get_extensions_list()
            num_bits: int = len(extensions).bit_length()
            predict_vuln_prob(
                predict_df,
                [f'extension_{num}' for num in range(num_bits + 1)],
                group,
                'file'
            )
    else:
        log(
            'error',
            "There is no 'fusion' folder in the path %s",
            subscription_path
        )
    return success
