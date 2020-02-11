#!/usr/bin/env bash

set -e

function print_tutorial() {
  echo "Use:"
  echo "  $0 username subscription CIDR"
  echo ""
  echo "Examples:"
  echo "  $0 kamadoatfluid gmail 192.168.1.1/32"
  echo "  $0 kamadoatfluid gmail \"192.168.0.0/16 or 10.0.0.0/8\""
  echo ""
  echo "Stop execution with Ctrl+C."
}

function print_error() {
  echo "Error:"
  echo "  $1"
  echo ""
  print_tutorial
  exit 1
}

function check_arguments() {
  if [ $# -ne 3 ]; then
    print_error "Not enough arguments."
  fi
}

function check_non_root() {
  if [ "$EUID" -eq 0 ]; then
    print_error "Don't run this script as root."
  fi
}

# Entry point
echo "Network traffic recorder."
echo ""
check_arguments "${@}"
check_non_root


non_root_user="$USER"

name="$(echo "$1" | tr '[:upper:]' '[:lower:]')"
subs="$(echo "$2" | tr '[:upper:]' '[:lower:]')"

file_dir="/var/tmp/pcap"
file_date=$(date --utc '+%Y-%m-%dT%H:%M:%SZ')
file_name="$file_dir/${name}_${subs}_${file_date}.pcap"

echo "Syncing hour..."
sudo ntpdate -v -u us.pool.ntp.org

echo "Creating output directory if not exists..."
echo "  $file_dir"
mkdir --parents "$file_dir"

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
    -C 1 \
    -w "$file_name"
