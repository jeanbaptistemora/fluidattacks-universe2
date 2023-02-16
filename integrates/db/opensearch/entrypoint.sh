# shellcheck shell=bash

function serve {
  : \
    && info "Launching OpenSearch" \
    && java \
      -Xms500m \
      -Xmx500m \
      -Dlog4j2.disable.jmx=true \
      -Dopensearch.distribution.type="tar" \
      -Dopensearch.path.conf="__argOpensearch__/config" \
      -Dopensearch.path.home="__argOpensearch__" \
      -classpath "__argOpensearch__/lib/*" \
      "org.opensearch.bootstrap.OpenSearch" \
      -Epath.data="${STATE}/data" \
      -Epath.logs="${STATE}/logs"
}

function serve_daemon {
  : \
    && kill_port "9200" \
    && { serve "${@}" & } \
    && wait_port 300 "0.0.0.0:9200" \
    && info "Opensearch is ready"
}

function main {
  : \
    && if [ "${DAEMON:-}" = "true" ]; then
      serve_daemon "${@}"
    else
      serve "${@}"
    fi
}

main "${@}"
