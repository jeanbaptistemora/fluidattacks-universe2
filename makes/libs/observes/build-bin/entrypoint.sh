# shellcheck shell=bash

source '__envPackage__'

'__envPython__' -c '__envEntrypoint__ as entrypoint; entrypoint()' "${@}"
