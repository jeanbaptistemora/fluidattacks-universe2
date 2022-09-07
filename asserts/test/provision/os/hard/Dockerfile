# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

FROM alpine:latest

RUN apk update && apk upgrade && apk add openssh clamav sudo
RUN ssh-keygen -A && \
    adduser -D -s /bin/sh nonpriv && \
    echo "root:Puef8poh2tei9AeB" | chpasswd && \
    echo "nonpriv:ahgh7xee9eewaeGh" | chpasswd && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config

CMD umask 0027 && /usr/sbin/sshd -D
