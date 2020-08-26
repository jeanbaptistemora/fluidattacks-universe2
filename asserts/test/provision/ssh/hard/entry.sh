#!/bin/sh

echo "Fluid Asserts - SSH Mock server - Hard"

exec /usr/sbin/sshd -D -e -f /etc/ssh/sshd_config
