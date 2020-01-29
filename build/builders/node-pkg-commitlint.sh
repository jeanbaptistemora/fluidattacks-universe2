# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcPackageDotJson}" root/src/repo/package.json

rules_name='commitlint.config.js'
parser_name='parser-preset.js'
base_repo='https://gitlab.com/fluidattacks/public'
base_url="${base_repo}/raw/master/commitlint-configs/others"
rules_url="${base_url}/${rules_name}"
parser_url="${base_url}/${parser_name}"

curl "${rules_url}" > "root/src/repo/${rules_name}"
curl "${parser_url}" > "root/src/repo/${parser_name}"

(
  cd root/src/repo
  HOME=. npm install --unsafe-perm
)

mkdir "${out}"
mv root/src/repo/* "${out}"
