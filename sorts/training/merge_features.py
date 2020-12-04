#!/usr/bin/env python3

# Standard Libraries
import os
import tempfile

# Third-party Libraries
import boto3
import pandas as pd
from pandas import DataFrame


if __name__ == '__main__':
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket('sorts')
    with tempfile.TemporaryDirectory() as tmpdir:
        for obj in s3_bucket.objects.filter(Prefix='features'):
            filename: str = os.path.basename(obj.key)
            s3_bucket.download_file(obj.key, os.path.join(tmpdir, filename))
        complete_filename: str = 'all_features.csv'
        complete_path: str = os.path.join(tmpdir, complete_filename)
        complete_features: DataFrame = pd.DataFrame()
        for file in os.listdir(tmpdir):
            features: DataFrame = pd.read_csv(os.path.join(tmpdir, file))
            complete_features = pd.concat([complete_features, features])
        complete_features.reset_index(drop=True, inplace=True)
        complete_features.to_csv(complete_path, index=False)
        s3_bucket.upload_file(complete_path, f'features/{complete_filename}')
