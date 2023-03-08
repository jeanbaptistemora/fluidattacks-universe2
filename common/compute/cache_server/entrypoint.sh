# shellcheck shell=bash

function generateConfig {
  local database_path="${1}"
  local storage_path="${2}"
  echo """
# Socket address to listen on
listen = \"[::]:8085\"
allowed-hosts = []
token-hs256-secret-base64 = \"VzloNEhRMWh5Qk9GT294bnJCbVFFaVRzT1IxeXgwR0dVVG1HNjRteHBzM2U0MzVOUjJBT2lJZThkUk5ZcGRaeGRPVGNzS3hpVFlSbGZ4WVU4TlRURWZjV1F0aWo1WGp3bmZmWUVMbUxJSjVqMEc5cGJDQUFsR0RCbDFwTG9QeTE=\"
[database]
url = \"${database_path}\"
[storage]
type = \"local\"
path = \"${storage_path}\"
[chunking]
nar-size-threshold = 65536 # chunk files that are 64 KiB or larger
min-size = 16384            # 16 KiB
avg-size = 65536            # 64 KiB
max-size = 262144           # 256 Ki
[compression]
type = \"zstd\"
[garbage-collection]
interval = \"12 hours\"
    """

}

function main {
  local configPath="$HOME/.config/attic/server.toml"

  mkdir -p "${HOME}/.config/attic/" \
    && mkdir -p "${HOME}/.local/share/attic/storage" \
    && sqlite3 "${HOME}/.local/share/attic/server.db" "VACUUM;" \
    && generateConfig "sqlite://${HOME}/.local/share/attic/server.db" "${HOME}/.local/share/attic/storage" > "${configPath}" \
    && atticadm -f "${configPath}" make-token --sub compute --validity '1 year' --pull 'compute' --push 'compute' --create-cache 'compute' \
    && atticd --config "${configPath}"
}

main "${@}"
