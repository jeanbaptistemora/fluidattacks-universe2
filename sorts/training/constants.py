# Third party libraries
import boto3


S3_BUCKET_NAME: str = 'sorts'
S3_RESOURCE = boto3.resource('s3')
S3_BUCKET = S3_RESOURCE.Bucket(S3_BUCKET_NAME)
