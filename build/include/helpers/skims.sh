# shellcheck shell=bash

function helper_skims_aws_login {
  local user="${1}"
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY

      if [ "${user}" = 'dev' ]
      then
            AWS_ACCESS_KEY_ID="${SKIMS_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SKIMS_DEV_AWS_SECRET_ACCESS_KEY}"
      elif [ "${user}" = 'prod' ]
      then
            AWS_ACCESS_KEY_ID="${SKIMS_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SKIMS_PROD_AWS_SECRET_ACCESS_KEY}"
      else
            echo '[ERROR] either prod or dev must be passed as arg' \
        &&  return 1
      fi \
  &&  echo "[INFO] Logging into AWS with ${user} credentials" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

function helper_skims_compute_version {
  poetry run python -c 'if True:
    import time
    now=time.gmtime()
    minutes_month=(
      (now.tm_mday - 1) * 1440
      + now.tm_hour * 60
      + now.tm_min
    )
    print(time.strftime(f"%y.%m.{minutes_month}"))
  '
}

function helper_skims_compile_ast {
  export CLASSPATH
  export srcExternalANTLR4
  local grammars=(
    Java9
  )

      echo '[INFO] Compiling grammars' \
  &&  pushd skims/static/ast/ \
    &&  export CLASSPATH=".:${srcExternalANTLR4}:${CLASSPATH:-}" \
    &&  for grammar in "${grammars[@]}"
        do
              echo "[INFO] Processing: ${grammar}" \
          &&  java -jar "${srcExternalANTLR4}" src/main/java/ast/Java9.g4 \
          &&  echo "[INFO] Compiling: ${grammar}" \
          &&  javac -Werror src/main/java/ast/Java9*.java \

        done \
    &&  echo '[INFO] Building AST tool' \
    &&  gradle installDist \
  &&  popd \
  ||  return 1
}
