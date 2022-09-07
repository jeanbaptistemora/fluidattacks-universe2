# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

FROM registry.gitlab.com/fluidattacks/product/asserts/mysql_os:hard

ENV MYSQL_PWD=something

ADD dot_mysqlhis /home/.mysql_history

RUN sed -i -e '/^mysql/s|/sbin/nologin|/bin/sh|g' /etc/passwd
