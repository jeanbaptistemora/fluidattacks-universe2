#!/bin/sh

# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

set -o errexit

execute_query() {
  mysql -uroot --password="${MYSQL_ROOT_PWD}" -e "$1"
}

# Enable old passwords. check: old_passwords_enabled
execute_query "SET @@GLOBAL.old_passwords=1;"
