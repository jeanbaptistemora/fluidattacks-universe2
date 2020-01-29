# shellcheck shell=bash

export YES='1'
export NO='0'

export NIX_BUILD_CORES='0'
export NIX_BUILD_MAX_JOBS='auto'
export NIXPKGS_ALLOW_UNFREE="${NO}"

export TEST_MARKERS=(
  all
  cloud_aws_api
  cloud_aws_cloudformation
  cloud_aws_terraform
  cloud_azure
  cloud_gcp
  cloud_kubernetes
  db
  format
  helper
  iot
  lang_core
  lang_csharp
  lang_docker
  lang_dotnetconfig
  lang_html
  lang_java
  lang_javascript
  lang_php
  lang_python
  lang_rpgle
  lang_times
  ot
  proto_dns
  proto_ftp
  proto_git
  proto_graphql
  proto_http
  proto_ldap
  proto_rest
  proto_smb
  proto_smtp
  proto_ssh
  proto_ssl
  proto_tcp
  sca
  syst
  utils
)
