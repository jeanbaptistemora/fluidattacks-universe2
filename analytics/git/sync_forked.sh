#!/usr/bin/env bash

# Import functions
. <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
. toolbox/others.sh

aws_login

new_sops_env secrets-prod.yaml default \
  analytics_auth_redshift

echo "$analytics_auth_redshift" > /target_secret.json

for fork in {1..32}; do
  ( tap-git \
      --conf /config.json \
      --with-metrics \
      --threads 32 \
      --fork-id $fork > git_part$fork ) &
done

wait

cat git_part{1..32} \
  | target-redshift \
      --auth /target_secret.json \
      --drop-schema \
      --schema-name "git"

rm -f git_part{1..32}
rm -f /target_secret.json
