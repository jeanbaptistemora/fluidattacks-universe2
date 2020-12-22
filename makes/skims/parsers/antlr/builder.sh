# shellcheck shell=bash

source "${makeDerivation}"

export CLASSPATH="${envANTLR}:${CLASSPATH:-}"

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
  &&  gradle installDist \
  &&  mv "${PWD}" "${out}" \
  ||  return 1
}

main "${@}"
