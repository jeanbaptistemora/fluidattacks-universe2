# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# Imagen base oficial del linux mas seguro y pequeno
FROM alpine:3.8

# Adiciona el servidor LDAP
RUN apk update \
    && apk upgrade \
    && apk add --no-cache openldap openldap-back-mdb \
    && rm -rf /var/cache/apk/* \
    && mkdir -p /run/openldap

# Expone los puertos LDAP
EXPOSE 389 636

# Primer comando que se ejecutara por completo
CMD /usr/sbin/slapd -d 256
