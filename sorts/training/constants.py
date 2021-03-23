# Standard libraries
from typing import (
    Dict,
    List
)

# Third party libraries
import boto3


S3_BUCKET_NAME: str = 'sorts'
S3_RESOURCE = boto3.resource('s3')
S3_BUCKET = S3_RESOURCE.Bucket(S3_BUCKET_NAME)

FEATURES_DICTS: Dict[str, str] = {
    'num_commits': 'CM',
    'num_unique_authors': 'AU',
    'file_age': 'FA',
    'midnight_commits': 'MC',
    'risky_commits': 'RC',
    'seldom_contributors': 'SC',
    'num_lines': 'LC',
    'busy_file': 'BF',
    'commit_frequency': 'CF'
}
RESULT_HEADERS: List[str] = [
    'Model',
    'Features',
    'Precision',
    'Recall',
    'F1',
    'Overfit'
]
