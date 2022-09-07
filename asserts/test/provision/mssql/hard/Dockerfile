# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

FROM mcr.microsoft.com/mssql/server:2017-latest

ENV ACCEPT_EULA Y
ENV SA_PASSWORD fluidasserts123.

ENV DB_USER test_user
ENV DB_PASSWORD Fluid1234.
ENV DB_NAME test_db

COPY . /scripts
