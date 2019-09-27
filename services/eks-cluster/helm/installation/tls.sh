#!/usr/bin/env bash

generate_key() {

  # Generate key

  set -e

  openssl genrsa -out "$1" 4096
}

generate_ca_cert() {

  # Generate ca

  set -e

  openssl req \
    -key "$1" \
    -new -x509 \
    -days 365 \
    -sha256 \
    -out "$2" \
    -extensions v3_ca \
    -subj "/C=US/ST=CA/L=San Francisco/O=Fluid Attacks/OU=IT Department/CN=fluidattacks.cluster.helm"
}

generate_csr() {

  # Generate csr

  set -e

  local CERT_INFO

  openssl req \
    -key "$1" \
    -new \
    -sha256 \
    -out "$2" \
    -subj "/C=US/ST=CA/L=San Francisco/O=Fluid Attacks/OU=IT Department/CN=fluidattacks.user.helm"
}

sign_csr() {

  # Sign csr with a ca to make it crt

  set -e

  openssl x509 -req -CAkey "$1" -CA "$2" -CAcreateserial -in "$3" -out "$4" -days 90
}

set_tls() {

  # Create files to set up Tiller with TLS

  set -e

  local CA_KEY
  local CA_CERT
  local TILLER_KEY
  local TILLER_CSR
  local TILLER_CERT

  CA_KEY='/tmp/ca.key'
  CA_CERT='/tmp/ca.cert'
  TILLER_KEY='/tmp/tiller.key'
  TILLER_CSR='/tmp/tiller.csr'
  TILLER_CERT='/tmp/tiller.crt'

  # Generate key and cert for CA
  generate_key $CA_KEY
  generate_ca_cert $CA_KEY $CA_CERT

  # Generate key and csr for user tiller
  generate_key $TILLER_KEY
  generate_csr $TILLER_KEY $TILLER_CSR

  # Generate crt for user tiller by signing its csr with the CA
  sign_csr $CA_KEY $CA_CERT $TILLER_CSR $TILLER_CERT

  # Remove unnecessary files
  rm "$CA_KEY" "$TILLER_CSR"

}
