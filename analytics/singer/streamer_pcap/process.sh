#!/usr/bin/env bash

set -e

echo "1. Extract data from the pcap files..."
rm -f .jsonstream
for file in /var/tmp/pcap/*; do
  # The name of the file contains metadata, extract it
  name=$(echo "${file}" | sed -E 's/\/var\/tmp\/pcap\/(.+)_.+_.+.pcap.*/\1/g')
  subs=$(echo "${file}" | sed -E 's/\/var\/tmp\/pcap\/.+_(.+)_.+.pcap.*/\1/g')
  date=$(echo "${file}" | sed -E 's/\/var\/tmp\/pcap\/.+_.+_(.+).pcap.*/"\1"/g')
  echo "  $file ($name, $subs, $date)"
  streamer-pcap "$file" \
    --kwarg "analyst=$name" \
    --kwarg "subscription=$subs" \
    --kwarg "recorded_date=$date" >> .jsonstream
done

echo "2. Transform streams..."
tap-json > .singer < .jsonstream
rm -f .jsonstream
