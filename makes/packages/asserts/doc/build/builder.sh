# shellcheck shell=bash

function execute_example_exploits {
  export yaml_key_b64='dGVzdHN0ZXN0c3Rlc3RzdGVzdHN0ZXN0c3Rlc3RzCg=='

  function striprun {
    $1 "$2" \
      | perl -pe 's/\e([^\[\]]|\[.*?[a-zA-Z]|\].*?\a)//g' \
      | tee "$2".out
  }

      mkdir resources \
  &&  cp sphinx/source/example/resources/secrets.yml ./resources/secrets.yml \
  &&  for example in sphinx/source/example/*.py; do
            striprun "python3" "$example" \
        ||  return 1
      done \
  &&  for example in sphinx/source/example/*.exp; do
            striprun "asserts" "$example" \
        ||  return 1
      done
}

function generate_doc {
  local checks_number

      mkdir -p output/ \
  &&  sphinx-apidoc -efM fluidasserts -o sphinx/source \
  &&  checks_number=$(grep -rIE '@(track|api)' fluidasserts/ | wc -l) \
  &&  sed -i "s/<CHECKS>/${checks_number}/" sphinx/source/index.rst \
  &&  sphinx-build -D version='v.__version__' -D release='v.__version__' \
        -b dirhtml -a sphinx/source/ output/ \
  &&  sphinx-build -b linkcheck sphinx/source output/review/ \
  &&  sphinx-build -b coverage  sphinx/source output/review/
}

function main {
      copy "${envSrcAssertsSphinx}" "${PWD}/sphinx" \
  &&  copy "${envSrcAssertsFluidasserts}" "${PWD}/fluidasserts" \
  &&  execute_example_exploits \
  &&  generate_doc \
  &&  mkdir "${out}" \
  &&  mv output "${out}/output"
}


main "${@}"
