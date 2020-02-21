#!/bin/sh

set -o errexit

execute_query () {
    mysql -uroot  --password="${MYSQL_ROOT_PWD}" -e "$1"
}

# Enable old passwords. check: old_passwords_enabled
execute_query "SET @@GLOBAL.old_passwords=1;"
