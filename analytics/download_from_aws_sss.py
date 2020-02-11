#!/usr/bin/env python3
"""A simple script to download from AWS S3."""

import sys
import json
import argparse

import boto3 as AWS_SDK


def create_access_point(auth_keys):
    """Create an access point.
    """

    session = AWS_SDK.session.Session(
        aws_access_key_id=auth_keys.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=auth_keys.get("AWS_SECRET_ACCESS_KEY"),
        region_name=auth_keys.get("AWS_DEFAULT_REGION")
    )

    sss_client = session.client('s3')
    sss_resource = session.resource('s3')

    return (sss_client, sss_resource)


def download_file(sss_resource, file):
    """Does the heavy lifting.
    """

    sss_resource.Bucket(
        file["bucket_name"]).download_file(
            file["object_key"],
            file["save_as"])


def main():
    """Usual entry point.
    """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-auth',
        help='JSON authentication file',
        type=argparse.FileType('r'))
    parser.add_argument(
        '-conf',
        help='JSON configuration file',
        type=argparse.FileType('r'))
    args = parser.parse_args()

    if not args.auth or not args.conf:
        parser.print_help()
        sys.exit(1)

    # load user params
    auth_keys = json.load(args.auth)
    file_list = json.load(args.conf)

    # Download
    (_, sss_resource) = create_access_point(auth_keys)
    for file in file_list:
        download_file(sss_resource, file)


if __name__ == "__main__":
    main()
