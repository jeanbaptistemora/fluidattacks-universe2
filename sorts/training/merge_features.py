#!/usr/bin/env python3

# Standard Libraries
import os
import tempfile

# Third-party Libraries
import numpy as np
import pandas as pd
from pandas import DataFrame

# Local libraries
from training.constants import S3_BUCKET


def main() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        for obj in S3_BUCKET.objects.filter(Prefix='features'):
            filename: str = os.path.basename(obj.key)
            local_file: str = os.path.join(tmpdir, filename)
            S3_BUCKET.download_file(obj.key, local_file)

        merged_filename: str = 'binary_encoded_training_data.csv'
        local_merged_file: str = os.path.join(tmpdir, merged_filename)
        remote_merged_file: str = f'training/{merged_filename}'
        merged_features: DataFrame = pd.DataFrame()
        for file in os.listdir(tmpdir):
            features: DataFrame = pd.read_csv(os.path.join(tmpdir, file))
            merged_features = pd.concat([merged_features, features])
        merged_features.reset_index(drop=True, inplace=True)

        # Change appropriate columns to numeric type for future filtering
        merged_features = merged_features.apply(pd.to_numeric, errors='ignore')
        # Drop all non-numeric columns
        merged_features = merged_features.select_dtypes([np.number])
        merged_features.to_csv(local_merged_file, index=False)
        S3_BUCKET.upload_file(local_merged_file, remote_merged_file)


if __name__ == '__main__':
    main()
