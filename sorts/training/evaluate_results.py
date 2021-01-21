#! /usr/bin/env python3

# Standard Libraries
import os
import tempfile

# Third-party Libraries
import boto3


# Constants
S3_BUCKET_NAME: str = 'sorts'


def main() -> None:
    s3_resource = boto3.resource('s3')
    s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)
    with tempfile.TemporaryDirectory() as tmp_dir:
        best_previous_model: str = ''
        best_current_model: str = ''
        best_f1: int = 0
        model_name_file: str = os.path.join(tmp_dir, 'best_model.txt')
        for obj in s3_bucket.objects.filter(Prefix='training-output'):
            # Since the best model has a generic name for easier download,
            # this TXT keeps track of the model name (class, f1, features)
            # so the final artifact is only replaced if there has been
            # an improvement
            if obj.key.endswith('.txt'):
                s3_resource.Object(S3_BUCKET_NAME, obj.key).download_file(
                    model_name_file
                )
                with open(model_name_file) as file:
                    best_previous_model = file.read()

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
                    s3_resource.Object(S3_BUCKET_NAME, obj.key).download_file(
                        os.path.join(tmp_dir, model_name)
                    )
                obj.delete()

        if best_previous_model != best_current_model:
            with open(model_name_file, 'w') as file:
                file.write(best_current_model)
            s3_resource.Object(
                S3_BUCKET_NAME,
                'training-output/best_model.txt'
            ).upload_file(model_name_file)
            s3_resource.Object(
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
