echo "$(vault read -field=analytics_auth_redshift secret/serves)" > /target_secret.json

for fork in {1..16}; do
  ( tap-git \
      --conf /config.json \
      --run-gitinspector \
      --with-metrics \
      --threads 16 \
      --fork-id $fork > git_part$fork ) &
done

wait

cat git_part{1..16} \
  | target-redshift \
      --auth /target_secret.json \
      --drop-schema \
      --schema-name "git"

rm -f git_part{1..16}
rm -f /target_secret.json
