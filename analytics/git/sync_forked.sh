#!/usr/bin/env bash

echo "$(vault read -field=analytics_auth_redshift secret/serves)" > /target_secret.json

for fork in {1..8}; do
  ( tap-git \
      --conf /config.json \
      --with-metrics \
      --threads 8 \
      --fork-id $fork > git_part$fork ) &
done

wait

cat git_part{1..8} \
  | target-redshift \
      --auth /target_secret.json \
      --drop-schema \
      --schema-name "git"

rm -f git_part{1..8}
rm -f /target_secret.json
