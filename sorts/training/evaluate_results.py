#! /usr/bin/env python3


import os
import sys
import tempfile
from training.constants import (
    MODEL_HYPERPARAMETERS,
    S3_BUCKET,
    S3_BUCKET_NAME,
    S3_RESOURCE,
)
from training.redshift import (
    db as redshift,
)
from typing import (
    Any,
    Dict,
    List,
)


def update_best_model_txt(model_name_file: str, best_model_name: str) -> None:
    if "tune" in best_model_name:
        with open(model_name_file, "a", encoding="utf8") as file:
            file.write(f"\n{best_model_name}")
    else:
        with open(model_name_file, "w", encoding="utf8") as file:
            file.write(best_model_name)


def get_best_model_name(model_name_file: str, mode: str = "train") -> str:
    # Since the best model has a generic name for easier download,
    # this TXT keeps track of the model name (class, f1, features)
    # so the final artifact is only replaced if there has been
    # an improvement
    best_model_lines: List[str] = []
    index: int = {"train": 0, "tune": -1}[mode]
    S3_RESOURCE.Object(
        S3_BUCKET_NAME, "training-output/best_model.txt"
    ).download_file(model_name_file)
    with open(model_name_file, encoding="utf8") as file:
        best_model_lines = file.read().splitlines()

    return best_model_lines[index]


def get_model_item(best_model_name: str) -> Dict[str, Any]:
    """Returns a dict containing model info ready to be sent to Redshift"""
    item: Dict[str, Any] = {}
    model_info = best_model_name.split("-")
    item["model"] = model_info[0]
    item["f_score"] = int(float(model_info[1]))
    item["features"] = ", ".join(
        part
        for part in model_info[2:]
        if len(part) == 2 and not part.isnumeric()
    ).upper()
    item["tuned_parameters"] = "n/a"
    if "tune" in best_model_name:
        tuned_parameters = MODEL_HYPERPARAMETERS[item["model"]].keys()
        tuned_parameters_values = model_info[item["features"].count(",") + 4 :]
        item["tuned_parameters"] = ", ".join(
            f"{key}:{value}"
            for key, value in dict(
                zip(tuned_parameters, tuned_parameters_values)
            ).items()
        )

    return item


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        best_current_model: str = ""
        model_name_file: str = os.path.join(tmp_dir, "best_model.txt")
        best_previous_model: str = get_best_model_name(
            model_name_file,
            sys.argv[1],
        )
        best_f1: float = float(best_previous_model.split("-")[1])
        for obj in S3_BUCKET.objects.filter(Prefix="training-output"):
            if (
                obj.key.endswith(".joblib")
                and obj.key != "training-output/model.joblib"
            ):
                # Models have the format 'class-f1-feat1-...-featn-.joblib'
                model_name: str = os.path.basename(obj.key).split(".joblib")[0]
                model_f1: float = float(model_name.split("-")[1])
                if model_f1 > best_f1:
                    best_f1 = model_f1
                    best_current_model = model_name
                    S3_RESOURCE.Object(S3_BUCKET_NAME, obj.key).download_file(
                        os.path.join(tmp_dir, model_name)
                    )
                obj.delete()

        if best_current_model and best_previous_model != best_current_model:
            update_best_model_txt(model_name_file, best_current_model)
            S3_RESOURCE.Object(
                S3_BUCKET_NAME, "training-output/best_model.txt"
            ).upload_file(model_name_file)
            S3_RESOURCE.Object(
                S3_BUCKET_NAME, "training-output/model.joblib"
            ).upload_file(
                os.path.join(tmp_dir, best_current_model),
                ExtraArgs={"ACL": "public-read"},
            )
            redshift.insert("models", get_model_item(best_current_model))
            print("[INFO] There is a new improved model available")
        else:
            print("[INFO] There have not been any improvements in the model")


if __name__ == "__main__":
    main()
