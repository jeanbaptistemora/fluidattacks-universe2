#!/bin/sh

# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

echo "Fluid Asserts - SSH Mock server - Weak"

exec /usr/sbin/sshd -D -e -f /etc/ssh/sshd_config
