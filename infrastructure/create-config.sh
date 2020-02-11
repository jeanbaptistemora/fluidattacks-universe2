#!/usr/bin/env bash
set -e

go get github.com/checkr/s3-sync/cmd

{
  echo "source:"
  echo "  account_number: ${OLD_AWS_ID}"
  echo "  aws_access_key_id: ${OLD_AWS_ACCESS_KEY_ID}"
  echo "  aws_secret_access_key: ${OLD_AWS_SECRET_ACCESS_KEY}"
  echo "  aws_region: us-east-1"
  echo ""
  echo "destination:"
  echo "  account_number: ${AWS_ID}"
  echo "  aws_user: ${AWS_USER}"
  echo "  aws_access_key_id: ${AWS_ACCESS_KEY_ID}"
  echo "  aws_secret_access_key: ${AWS_SECRET_ACCESS_KEY}"
  echo "  aws_region: us-east-1"
  echo "  enable_bucket_versioning: false"
  echo "  sync_sse: AES256"
  echo ""
  echo "buckets:"
  echo "  ${OLD_FI_AWS_S3_BUCKET}: ${FI_AWS_S3_BUCKET}"
} >> s3-sync/config-prod.yaml
