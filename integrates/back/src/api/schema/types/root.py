from api.resolvers.git_root import (
    credentials,
    download_url,
    environment_secrets,
    git_environment_urls,
    last_machine_executions,
    secrets,
    upload_url,
    vulnerabilities,
)
from ariadne import (
    ObjectType,
)

GITROOT: ObjectType = ObjectType("GitRoot")
GITROOT.set_field("credentials", credentials.resolve)
GITROOT.set_field("lastMachineExecutions", last_machine_executions.resolve)
GITROOT.set_field("secrets", secrets.resolve)
GITROOT.set_field("gitEnvironmentUrls", git_environment_urls.resolve)
GITROOT.set_field("downloadUrl", download_url.resolve)
GITROOT.set_field("uploadUrl", upload_url.resolve)
GITROOT.set_field("vulnerabilities", vulnerabilities.resolve)

ENVIRONMENT_URL: ObjectType = ObjectType("GitEnvironmentUrl")
ENVIRONMENT_URL.set_field("secrets", environment_secrets.resolve)

IPROOT: ObjectType = ObjectType("IPRoot")
IPROOT.set_field("vulnerabilities", vulnerabilities.resolve)

URLROOT: ObjectType = ObjectType("URLRoot")
URLROOT.set_field("vulnerabilities", vulnerabilities.resolve)
