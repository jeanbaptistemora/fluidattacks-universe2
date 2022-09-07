# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

FROM alpine:3.9

ENV FLAVOR weak

EXPOSE 25/tcp

RUN apk update && apk upgrade && apk add postfix

COPY etc_postfix_main.cf-weak /etc/postfix/main.cf

ENTRYPOINT ["/usr/libexec/postfix/master", "-c", "/etc/postfix", "-d"]
