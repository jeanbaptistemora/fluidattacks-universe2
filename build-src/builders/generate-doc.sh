# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcDeploy}" root/src/repo/deploy
cp -r --no-preserve=mode,ownership \
  "${srcDotGit}" root/src/repo/.git
cp -r --no-preserve=mode,ownership \
  "${srcDotMailmap}" root/src/repo/.mailmap
cp -r --no-preserve=mode,ownership \
  "${srcFluidasserts}" root/src/repo/fluidasserts
cp -r --no-preserve=mode,ownership \
  "${srcSphinx}" root/src/repo/sphinx

cp -r --no-preserve=mode,ownership \
  "${pyPkgFluidasserts}/"* root/python
cp -r --no-preserve=mode,ownership \
  "${pyPkgGitFame}/"* root/python
cp -r --no-preserve=mode,ownership \
  "${pyPkgSphinx}/"* root/python

chmod +x root/python/site-packages/bin/asserts
chmod +x root/python/site-packages/bin/git-fame
chmod +x root/python/site-packages/bin/sphinx-apidoc
chmod +x root/python/site-packages/bin/sphinx-build

PATH="${PWD}/root/python/site-packages/bin:${PATH}"
PYTHONPATH="${PYTHONPATH}:${PWD}/root/python/site-packages"

pushd root/src/repo

function striprun {
  $1 "$2" \
    | perl -pe 's/\e([^\[\]]|\[.*?[a-zA-Z]|\].*?\a)//g' \
    | tee "$2".out
}

function execute_example_exploits {
  export yaml_key_b64

  # Setup the exploits environment
  mkdir resources
  cp sphinx/source/example/resources/secrets.yml ./resources/secrets.yml
  yaml_key_b64='dGVzdHN0ZXN0c3Rlc3RzdGVzdHN0ZXN0c3Rlc3RzCg=='

  # Execute the examples and save their output
  for example in sphinx/source/example/*.py; do
    striprun "python3" "$example"
  done
  for example in sphinx/source/example/*.exp; do
    striprun "asserts" "$example"
  done
}

function generate_credits {
  local current_branch

  echo >> sphinx/source/credits.rst

  current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'master')

  if test "${current_branch}" = "master"
  then
    echo 'running git-fame... this may take a loooong time'
    git-fame \
        -C \
        --log=ERROR \
        --silent-progress \
        --ignore-whitespace \
        --cost=cocomo \
      | grep -viE '^total [a-z]+: [0-9]+(\.[0-9]+)?$' \
      | grep -vP '^\D+?\d+\D+?0' \
      | grep -vP 'Jane Doe' \
      | tee -a sphinx/source/credits.rst
  else
    echo 'the table of credits will be generated in the master branch!' \
      | tee -a sphinx/source/credits.rst
  fi

  cat sphinx/source/credits.rst.footer >> sphinx/source/credits.rst
}

function build_doc {
  local version
  local checks_number

  # HTML must go to public/ for gitlab pages
  mkdir -p public/

  # Generate e: separate page per module f: overwrite M: module doc first
  sphinx-apidoc -efM fluidasserts -o sphinx/source

  version=$(python3 ./deploy/get_version.py)
  checks_number=$(grep -rIE '@(track|api)' fluidasserts/ | wc -l)

  sed -i "s/<CHECKS>/${checks_number}/" sphinx/source/index.rst

  sphinx-build -D version="v.${version}" -D release="v.${version}" \
               -b dirhtml -a sphinx/source/ public/
  sphinx-build -b linkcheck sphinx/source public/review/
  sphinx-build -b coverage  sphinx/source public/review/
}

execute_example_exploits
generate_credits
build_doc

mv public "${out}"
