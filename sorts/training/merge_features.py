#!/usr/bin/env python3


import numpy as np
import os
import pandas as pd
from pandas import (
    DataFrame,
)
import tempfile
from training.constants import (
    DATASET_THRESHOLD,
    S3_BUCKET,
)
from training.redshift import (
    db as redshift,
)


def copy_dataset(dataset_filename: str, dataset_copy_filename: str) -> None:
    """Makes a copy of current dataset before generating the new one"""
    S3_BUCKET.copy(
        {"Bucket": S3_BUCKET.name, "Key": f"training/{dataset_filename}"},
        f"training/{dataset_copy_filename}",
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        for obj in S3_BUCKET.objects.filter(Prefix="features"):
            filename: str = os.path.basename(obj.key)
            local_file: str = os.path.join(tmpdir, filename)
            S3_BUCKET.download_file(obj.key, local_file)

        merged_filename: str = "binary_encoded_training_data.csv"
        backup_filename: str = merged_filename.replace(".csv", "_prev.csv")
        local_merged_file: str = os.path.join(tmpdir, merged_filename)
        remote_merged_file: str = f"training/{merged_filename}"

        # Save current versions as prev one
        copy_dataset(merged_filename, backup_filename)

        # Merge groups features
        merged_features: DataFrame = pd.DataFrame()
        redshift.delete("features")
        for file in os.listdir(tmpdir):
            features: DataFrame = pd.read_csv(os.path.join(tmpdir, file))
            merged_features = pd.concat([merged_features, features])
            redshift.insert(
                "features",
                {
                    "group_name": file.split("_")[0],
                    "n_vulns": len(features.index),
                },
            )
        merged_features.reset_index(drop=True, inplace=True)

        # Change appropriate columns to numeric type for future filtering
        merged_features = merged_features.apply(pd.to_numeric, errors="ignore")
        # Drop all non-numeric columns
        merged_features = merged_features.select_dtypes([np.number])
        merged_features.to_csv(local_merged_file, index=False)
        S3_BUCKET.upload_file(local_merged_file, remote_merged_file)

        n_rows = len(merged_features.index)
        if n_rows < DATASET_THRESHOLD * 1000:
            # Replace just generated dataset by its backup
            copy_dataset(backup_filename, merged_filename)

        redshift.insert("dataset", {"n_rows": n_rows})
        print(
            "[INFO]: Our current dataset has a total number of "
            f"{n_rows} elements"
        )


if __name__ == "__main__":
    main()
