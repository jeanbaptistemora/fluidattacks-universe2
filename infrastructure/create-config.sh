#!/usr/bin/env bash
set -e

go get github.com/checkr/s3-sync/cmd

echo "source:" >> s3-sync/config-prod.yaml
echo "  account_number: $OLD_AWS_ID" >> s3-sync/config-prod.yaml
echo "  aws_access_key_id: $OLD_AWS_ACCESS_KEY_ID" >> s3-sync/config-prod.yaml
echo "  aws_secret_access_key: $OLD_AWS_SECRET_ACCESS_KEY" >> s3-sync/config-prod.yaml
echo "  aws_region: us-east-1" >> s3-sync/config-prod.yaml
echo "" >> s3-sync/config-prod.yaml
echo "destination:" >> s3-sync/config-prod.yaml
echo "  account_number: $AWS_ID" >> s3-sync/config-prod.yaml
echo "  aws_user: $AWS_USER" >> s3-sync/config-prod.yaml
echo "  aws_access_key_id: $AWS_ACCESS_KEY_ID" >> s3-sync/config-prod.yaml
echo "  aws_secret_access_key: $AWS_SECRET_ACCESS_KEY" >> s3-sync/config-prod.yaml
echo "  aws_region: us-east-1" >> s3-sync/config-prod.yaml
echo "  enable_bucket_versioning: false" >> s3-sync/config-prod.yaml
echo "  sync_sse: AES256" >> s3-sync/config-prod.yaml
echo "" >> s3-sync/config-prod.yaml
echo "buckets:" >> s3-sync/config-prod.yaml
echo "  $OLD_FI_AWS_S3_BUCKET: $FI_AWS_S3_BUCKET" >> s3-sync/config-prod.yaml
