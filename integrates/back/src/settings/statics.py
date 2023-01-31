from context import (
    CI_COMMIT_REF_NAME,
    FI_ENVIRONMENT,
    STARTDIR,
)

AWS_S3_CUSTOM_DOMAIN: str = (
    f"integrates.front.{FI_ENVIRONMENT}.fluidattacks.com"
)
STATIC_URL: str = f"https://{AWS_S3_CUSTOM_DOMAIN}/{CI_COMMIT_REF_NAME}/static"
TEMPLATES_DIR: str = f"{STARTDIR}/integrates/back/src/app/templates"
