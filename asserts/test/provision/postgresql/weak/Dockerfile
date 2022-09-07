# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

FROM postgres:12-alpine

ENV POSTGRES_DB='postgres'
ENV POSTGRES_USER='postgres'
ENV POSTGRES_PASSWORD='postgres'

COPY --chown=postgres:postgres *.sql /docker-entrypoint-initdb.d
