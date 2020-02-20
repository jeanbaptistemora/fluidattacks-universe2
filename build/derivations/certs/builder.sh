# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"

mkdir "${out}"

openssl req \
  -new \
  -subj '/C=CO' \
  -subj '/ST=Antioquia' \
  -subj '/L=Medellin' \
  -subj '/O=Fluid' \
  -subj '/CN=fluidattacks.com' \
  -subj '/emailAddress=kamado@fluidattacks.com' \
  -newkey 'rsa:2048' \
  -days '365' \
  -nodes \
  -x509 \
  -keyout "${out}/fluidla.key" \
  -out "${out}/fluidla.crt"

openssl x509 \
  -inform 'pem' \
  -noout \
  -text \
  -in "${out}/fluidla.crt"
