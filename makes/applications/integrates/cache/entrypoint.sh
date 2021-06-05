# shellcheck shell=bash

function serve {
  local cluster_addrs=()
  local cluster_path='.Cache'

  echo '[INFO] Launching Redis' \
    && rm -rf "${cluster_path}" \
    && makes-kill-port 26379 \
    && for port in 6379 6380 6381; do
      echo "[INFO] Configuring replica ${port}" \
        && makes-kill-port "${port}" \
        && mkdir -p "${cluster_path}/${port}" \
        && pushd "${cluster_path}/${port}" \
        && {
          echo 'appendonly yes' \
            && echo 'cluster-config-file nodes.conf' \
            && echo 'cluster-enabled yes' \
            && echo 'cluster-node-timeout 5000' \
            && echo 'cluster-slave-validity-factor 1' \
            && echo "port ${port}"

        } > redis.conf \
        && { redis-server redis.conf & } \
        && popd \
        && cluster_addrs+=("127.0.0.1:${port}") \
        || return 1
    done \
    && makes-wait 10 "${cluster_addrs[@]}" \
    && redis-cli \
      --cluster create "${cluster_addrs[@]}" \
      --cluster-replicas 0 \
      --cluster-yes \
    && makes-done 26379 \
    && wait
}

function serve_daemon {
  makes-kill-port 26379 \
    && { serve "${@}" & } \
    && makes-wait 60 localhost:26379
}

function main {
  if test "${DAEMON:-}" = 'true'; then
    serve_daemon "${@}"
  else
    serve "${@}"
  fi
}

main "${@}"
