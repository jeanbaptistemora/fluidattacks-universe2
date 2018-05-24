#!/bin/bash
echo "$FI_SSL_CERT" | base64 -di > "/etc/ssl/certs/fluidla.crt"
echo "$FI_SSL_KEY" | base64 -di > "/etc/ssl/private/fluidla.key"