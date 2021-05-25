from __init__ import (
    CI_COMMIT_REF_NAME,
    FI_ENVIRONMENT,
)


AWS_S3_CUSTOM_DOMAIN: str = (
    f"integrates.front.{FI_ENVIRONMENT}.fluidattacks.com"
)
STATIC_URL: str = f"https://{AWS_S3_CUSTOM_DOMAIN}/{CI_COMMIT_REF_NAME}/static"
TEMPLATES_DIR: str = "back/packages/modules/app/templates"
