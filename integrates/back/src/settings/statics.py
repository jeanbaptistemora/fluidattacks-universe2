# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    CI_COMMIT_REF_NAME,
    FI_ENVIRONMENT,
)

AWS_S3_CUSTOM_DOMAIN: str = (
    f"integrates.front.{FI_ENVIRONMENT}.fluidattacks.com"
)
STATIC_URL: str = f"https://{AWS_S3_CUSTOM_DOMAIN}/{CI_COMMIT_REF_NAME}/static"
TEMPLATES_DIR: str = "back/src/app/templates"
