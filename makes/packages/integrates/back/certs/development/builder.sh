# shellcheck shell=bash

function main {
      mkdir "${out}" \
  &&  openssl req \
        -days '365' \
        -keyout "${out}/cert.key" \
        -new \
        -newkey 'rsa:2048' \
        -nodes \
        -out "${out}/cert.crt" \
        -subj '/C=CO' \
        -subj '/CN=fluidattacks.com' \
        -subj '/emailAddress=development@fluidattacks.com' \
        -subj '/L=Medellin' \
        -subj '/O=Fluid' \
        -subj '/ST=Antioquia' \
        -x509 \
  &&  openssl x509 \
        -in "${out}/cert.crt" \
        -inform 'pem' \
        -noout \
        -text
}

main "${@}"
