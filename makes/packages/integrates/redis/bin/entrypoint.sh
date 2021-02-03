# shellcheck shell=bash

function main {
  local cluster_addrs=()
  local cluster_path='integrates/.Redis'

    echo '[INFO] Launching Redis' \
  &&  rm -rf "${cluster_path}" \
  &&  for port in 6379 6380 6381
      do
            echo "[INFO] Configuring replica ${port}" \
        &&  '__envKillPidListeningOnPort__' "${port}" \
        &&  mkdir -p "${cluster_path}/${port}" \
        &&  pushd "${cluster_path}/${port}" \
          &&  {
                    echo 'appendonly yes' \
                &&  echo 'cluster-config-file nodes.conf' \
                &&  echo 'cluster-enabled yes' \
                &&  echo 'cluster-node-timeout 5000' \
                &&  echo 'cluster-slave-validity-factor 1' \
                &&  echo "port ${port}" \

              } > redis.conf \
          &&  { __envRedisServer__ redis.conf & } \
        &&  popd \
        &&  cluster_addrs+=( "127.0.0.1:${port}" ) \
        ||  return 1
      done \
  &&  __envWait__ 10 "${cluster_addrs[@]}" \
  &&  __envRedisCli__ \
        --cluster create "${cluster_addrs[@]}" \
        --cluster-replicas 0 \
        --cluster-yes \
  &&  wait
}

main "${@}"
