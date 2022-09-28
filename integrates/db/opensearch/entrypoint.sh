# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function opensearch {
  : \
    && java \
      -Xms1g \
      -Xmx1g \
      -Dlog4j2.disable.jmx=true \
      -Dopensearch.distribution.type="tar" \
      -Dopensearch.path.home="__argOpensearch__" \
      -Dopensearch.path.conf="__argOpensearch__/config" \
      -classpath "__argOpensearch__/lib/*" \
      org.opensearch.bootstrap.OpenSearch \
      "$@" \
    || return 1
}

function main {
  : \
    && opensearch \
      -Epath.data="${STATE}/data" \
      -Epath.logs="${STATE}/logs" \
    || return 1
}

main "${@}"
