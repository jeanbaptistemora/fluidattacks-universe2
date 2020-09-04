# shellcheck shell=bash

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
    &&  gradle build \
  &&  popd \
  ||  return 1
}
