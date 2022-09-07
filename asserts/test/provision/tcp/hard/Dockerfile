# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

FROM alpine:latest

EXPOSE 443

RUN apk update && apk upgrade && mkdir -p /run/apache2 && apk add apache2-ssl

CMD /usr/sbin/httpd -D FOREGROUND
