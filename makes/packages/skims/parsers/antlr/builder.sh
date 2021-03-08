# shellcheck shell=bash

function compile_antlr {
  java -jar "${envANTLR}" -no-listener -no-visitor "${@}"
}

function compile_java {
  javac -Werror "${@}"
}

function main {
  local languages=(
    CSharp
    Java9
    Scala
  )

      echo '[INFO] Copying parser' \
  &&  copy "${envSrc}" . \
  &&  for language in "${languages[@]}"
      do
            echo "[INFO] Building ANTLR-${language} parser" \
        &&  compile_antlr "src/main/java/parse/${language}"*'.g4' \
        &&  compile_java "src/main/java/parse/${language}"*'.java' \
        ||  return 1
      done \
  &&  gradle -g "$(mktemp -d)" installDist \
  &&  mv "${PWD}" "${out}" \
  &&  {
            echo "#! $(command -v bash)" \
        &&  echo \
        &&  for jar in "${out}/build/install/parse/lib/"*
            do
              echo "export CP=\"${jar}:\${CP:-}\""
            done \
        &&  echo \
        &&  echo "$(command -v java) -classpath \"\${CP}\" Parse \"\${@}\"" \

      } > "${out}/build/install/parse/bin/parse" \
  ||  return 1
}

main "${@}"
