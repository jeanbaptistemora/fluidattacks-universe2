# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import os

FI_AWS_OPENSEARCH_HOST = os.environ["AWS_OPENSEARCH_HOST"]
FI_AWS_REDSHIFT_DBNAME = os.environ.get("AWS_REDSHIFT_DBNAME")
FI_AWS_REDSHIFT_HOST = os.environ.get("AWS_REDSHIFT_HOST")
FI_AWS_REDSHIFT_PASSWORD = os.environ.get("AWS_REDSHIFT_PASSWORD")
FI_AWS_REDSHIFT_USER = os.environ.get("AWS_REDSHIFT_USER")
FI_DYNAMODB_HOST = os.environ["DYNAMODB_HOST"]
FI_DYNAMODB_PORT = os.environ["DYNAMODB_PORT"]
FI_ENVIRONMENT = os.environ["ENVIRONMENT"]
FI_GOOGLE_CHAT_WEBOOK_URL = os.environ["GOOGLE_CHAT_WEBOOK_URL"]
FI_WEBHOOK_POC_KEY = os.environ["WEBHOOK_POC_KEY"]
FI_WEBHOOK_POC_ORG = os.environ["WEBHOOK_POC_ORG"]
FI_WEBHOOK_POC_URL = os.environ["WEBHOOK_POC_URL"]
