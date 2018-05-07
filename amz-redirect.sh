#!/usr/bin/env bash

# This script solves the issue of 302 redirects from URLs without trailing
# slash to their counterparts with trailing slash in S3.
# It creates an S3 objetc in the URL without trailing slash which has
# a metadata that defines a 301 redirect to the URL with trailing slash.

PATTERN="output/"
PATTERN2="/index.html"

export AWS_ACCESS_KEY_ID="$FW_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="$FW_AWS_SECRET_ACCESS_KEY"

find output -iname '*.html' | while IFS= read -r FILE; do
  STRING=${FILE/$PATTERN/}
  NAME=${STRING/$PATTERN2/}
  if [[ ! $NAME = *".html" ]]; then
    aws s3api put-object --acl public-read \
    --bucket "$FW_S3_BUCKET_NAME" --key "$NAME" --content-type text/html \
    --website-redirect-location "/$NAME/";
  fi;
done
