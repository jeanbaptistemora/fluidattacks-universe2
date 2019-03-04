#!/usr/bin/env bash

set -e

if [ $# -ne 3 ]; then
  echo "Not enough arguments."
  echo ""
  echo "Use:"
  echo "  $0 username subscription CIDR"
  echo ""
  echo "Examples:"
  echo "  $0 kamadoatfluid gmail 192.168.1.1/32"
  echo "  $0 kamadoatfluid gmail \"192.168.0.0/16 or 10.0.0.0/8\""
  echo ""
  echo "Stop execution with Ctrl+C"
  exit -1
fi

non_root_user="$USER"

name="$(echo "$1" | tr '[:upper:]' '[:lower:]')"
subs="$(echo "$2" | tr '[:upper:]' '[:lower:]')"
cidr="$3"

file_date=$(date --utc '+%Y-%m-%dT%H:%M:%SZ')
file_name="/var/tmp/${name}_${subs}_${file_date}.pcap"

echo "Syncing hour..."
sudo ntpdate -v -u us.pool.ntp.org

echo "Recording session to:"
echo "  $file_name"
sudo tcpdump \
    --interface=any \
    --immediate-mode \
    --relinquish-privileges="$non_root_user" \
    -n \
    -xx \
    -vvv \
    -tttt \
    -w "$file_name"
