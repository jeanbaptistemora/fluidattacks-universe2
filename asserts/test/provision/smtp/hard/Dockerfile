# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

FROM registry.gitlab.com/fluidattacks/product/asserts/smtp:weak

ENV FLAVOR hard

EXPOSE 25/tcp

COPY etc_postfix_main.cf-hard /etc/postfix/main.cf

ENTRYPOINT ["/usr/libexec/postfix/master", "-c", "/etc/postfix", "-d"]
