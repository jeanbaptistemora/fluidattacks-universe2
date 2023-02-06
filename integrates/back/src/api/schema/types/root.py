from api.resolvers.git_environment_url import (
    secrets as environment_secrets,
)
from api.resolvers.git_root import (
    branch,
    cloning_status,
    created_at,
    credentials,
    download_url,
    environment,
    environment_urls,
    git_environment_urls,
    gitignore,
    includes_health_check,
    last_cloning_status_update,
    last_edited_at,
    last_edited_by,
    last_state_status_update,
    secrets,
    upload_url,
    url,
    use_vpn,
    vulnerabilities,
)
from api.resolvers.ip_root import (
    address,
    port as ip_port,
)
from api.resolvers.root import (
    nickname,
    state,
)
from api.resolvers.url_root import (
    host,
    path,
    port as url_port,
    protocol,
    query,
)
from ariadne import (
    ObjectType,
)

GITROOT: ObjectType = ObjectType("GitRoot")
GITROOT.set_field("branch", branch.resolve)
GITROOT.set_field("cloningStatus", cloning_status.resolve)
GITROOT.set_field("createdAt", created_at.resolve)
GITROOT.set_field("credentials", credentials.resolve)
GITROOT.set_field("lastEditedAt", last_edited_at.resolve)
GITROOT.set_field("lastEditedBy", last_edited_by.resolve)
GITROOT.set_field("downloadUrl", download_url.resolve)
GITROOT.set_field("environment", environment.resolve)
GITROOT.set_field("environmentUrls", environment_urls.resolve)
GITROOT.set_field("gitEnvironmentUrls", git_environment_urls.resolve)
GITROOT.set_field("gitignore", gitignore.resolve)
GITROOT.set_field("includesHealthCheck", includes_health_check.resolve)
GITROOT.set_field(
    "lastCloningStatusUpdate", last_cloning_status_update.resolve
)
GITROOT.set_field("lastStateStatusUpdate", last_state_status_update.resolve)
GITROOT.set_field("nickname", nickname.resolve)
GITROOT.set_field("secrets", secrets.resolve)
GITROOT.set_field("state", state.resolve)
GITROOT.set_field("uploadUrl", upload_url.resolve)
GITROOT.set_field("url", url.resolve)
GITROOT.set_field("useVpn", use_vpn.resolve)
GITROOT.set_field("vulnerabilities", vulnerabilities.resolve)

ENVIRONMENT_URL: ObjectType = ObjectType("GitEnvironmentUrl")
ENVIRONMENT_URL.set_field("secrets", environment_secrets.resolve)

IPROOT: ObjectType = ObjectType("IPRoot")
IPROOT.set_field("address", address.resolve)
IPROOT.set_field("nickname", nickname.resolve)
IPROOT.set_field("port", ip_port.resolve)
IPROOT.set_field("state", state.resolve)
IPROOT.set_field("vulnerabilities", vulnerabilities.resolve)

URLROOT: ObjectType = ObjectType("URLRoot")
URLROOT.set_field("host", host.resolve)
URLROOT.set_field("nickname", nickname.resolve)
URLROOT.set_field("path", path.resolve)
URLROOT.set_field("port", url_port.resolve)
URLROOT.set_field("protocol", protocol.resolve)
URLROOT.set_field("query", query.resolve)
URLROOT.set_field("secrets", secrets.resolve)
URLROOT.set_field("state", state.resolve)
URLROOT.set_field("vulnerabilities", vulnerabilities.resolve)
