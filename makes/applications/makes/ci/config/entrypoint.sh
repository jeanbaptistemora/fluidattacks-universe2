# shellcheck shell=bash

function main {
  local bastion_ip='192.168.3.11'
  local bastion_user='ubuntu'
  local config='config.toml'
  local init='init.sh'
  local tmp_file_1
  local tmp_file_2
  local secrets_to_replace=(
    autoscaling_token_1
    autoscaling_token_2
    autoscaling_token_3
    autoscaling_token_4
    autoscaling_access_key
    autoscaling_secret_key
    autoscaling_bastion_key_b64
  )

      echo '[INFO] Exporting secrets' \
  &&  aws_login_prod makes \
  &&  sops_export_vars makes/applications/serves/secrets/src/production.yaml "${secrets_to_replace[@]}" \
  &&  pushd makes/applications/makes/ci/src \
    &&  echo '[INFO] Creating temporary files' \
    &&  tmp_file_1="$(mktemp)" \
    &&  tmp_file_2="$(mktemp)" \
    &&  echo '[INFO] Adding bastion to known hosts' \
    &&  mkdir -p ~/.ssh \
    &&  touch ~/.ssh/known_hosts \
    &&  ssh-keyscan -H "${bastion_ip}" >> ~/.ssh/known_hosts \
    &&  echo '[INFO] Exporting bastion SSH key' \
    &&  echo -n "${autoscaling_bastion_key_b64}" | base64 -d > "${tmp_file_1}" \
    &&  ssh-keygen -y -f "${tmp_file_1}" > "${tmp_file_1}.pub" \
    &&  echo '[INFO] Executing test: $ sudo whoami' \
    &&  ssh -i "${tmp_file_1}" "${bastion_user}@${bastion_ip}" 'sudo whoami' \
    &&  echo '[INFO] Writing config with secrets' \
    &&  cp "${config}" "${tmp_file_2}" \
    &&  for secret in "${secrets_to_replace[@]}"
        do
                rpl "__${secret}__" "${!secret}" "${tmp_file_2}" \
            |&  grep 'Replacing' \
            |&  sed -E 's/with.*$//g' \
            ||  return 1
        done \
    &&  echo '[INFO] Moving file to bastion: config.toml to /etc/gitlab-runner/config.toml' \
    &&  scp -i "${tmp_file_1}" "${tmp_file_2}" "${bastion_user}@${bastion_ip}:/port/config.toml" \
    &&  ssh -i "${tmp_file_1}" "${bastion_user}@${bastion_ip}" \
          'sudo mv /port/config.toml /etc/gitlab-runner/config.toml' \
    &&  echo '[INFO] Moving file to bastion: init.sh to /etc/gitlab-runner/init.sh' \
    &&  scp -i "${tmp_file_1}" "${init}" "${bastion_user}@${bastion_ip}:/port/init.sh" \
    &&  ssh -i "${tmp_file_1}" "${bastion_user}@${bastion_ip}" \
              'sudo mv /port/init.sh /etc/gitlab-runner/init.sh' \
    &&  echo '[INFO] Reloading bastion config: /etc/gitlab-runner/config.toml' \
    &&  ssh -i "${tmp_file_1}" "${bastion_user}@${bastion_ip}" \
            'sudo killall -SIGHUP gitlab-runner' \
    &&  echo '[INFO] Removing temporary files' \
    &&  rm -rf "${tmp_file_1}" "${tmp_file_2}" \
  &&  popd \
  ||  return 1
}

main "${@}"
