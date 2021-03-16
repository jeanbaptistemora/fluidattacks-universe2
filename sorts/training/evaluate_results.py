#! /usr/bin/env python3

# Standard Libraries
import os
import tempfile

# Local libraries
from constants import (
    S3_BUCKET,
    S3_BUCKET_NAME,
    S3_RESOURCE
)


def get_best_model_name(model_name_file: str) -> str:
    # Since the best model has a generic name for easier download,
    # this TXT keeps track of the model name (class, f1, features)
    # so the final artifact is only replaced if there has been
    # an improvement
    best_model: str = ''
    S3_RESOURCE.Object(
        S3_BUCKET_NAME,
        'training-output/best_model.txt'
    ).download_file(model_name_file)
    with open(model_name_file) as file:
        best_model = file.read()

    return best_model


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        best_current_model: str = ''
        best_f1: int = 0
        model_name_file: str = os.path.join(tmp_dir, 'best_model.txt')
        best_previous_model: str = get_best_model_name(model_name_file)
        for obj in S3_BUCKET.objects.filter(Prefix='training-output'):
            if (
                obj.key.endswith('.joblib')
                and obj.key != 'training-output/model.joblib'
            ):
                # Models have the format 'class-f1-feat1-...-featn-.joblib'
                model_name: str = os.path.basename(obj.key)
                model_f1: int = int(model_name.split('-')[1])
                if model_f1 > best_f1:
                    best_f1 = model_f1
                    best_current_model = model_name
                    S3_RESOURCE.Object(S3_BUCKET_NAME, obj.key).download_file(
                        os.path.join(tmp_dir, model_name)
                    )
                obj.delete()

        if best_previous_model != best_current_model:
            with open(model_name_file, 'w') as file:
                file.write(best_current_model)
            S3_RESOURCE.Object(
                S3_BUCKET_NAME,
                'training-output/best_model.txt'
            ).upload_file(model_name_file)
            S3_RESOURCE.Object(
                S3_BUCKET_NAME,
                'training-output/model.joblib'
            ).upload_file(
                os.path.join(tmp_dir, best_current_model),
                ExtraArgs={'ACL': 'public-read'}
            )
            print('[INFO]: There is a new improved model available')
        else:
            print('[INFO]: There have not been any improvements in the model')


if __name__ == '__main__':
    main()
