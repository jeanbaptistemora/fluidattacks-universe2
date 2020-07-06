# Standard library
from typing import (
    Dict,
)

# Third party libraries
from storages.backends.s3boto3 import S3Boto3Storage

# Linters configuration
# pylint: disable=abstract-method
#   I don't need to override those other abstract methods, just this one


class IntegratesStaticFilesStorage(S3Boto3Storage):

    def get_object_parameters(self, name: str) -> Dict[str, str]:
        partial_object_parameters: Dict[str, Dict[str, str]] = {
            # Don't cache the front-end bundles
            'integrates/assets/dashboard': {
                'CacheControl': 'max-age=0',
            }
        }

        for partial_name, parameters in partial_object_parameters.items():
            if partial_name in name:
                return parameters

        return {}
