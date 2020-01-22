# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcBuildSrc}" root/src/repo/build-src

cd root/src/repo

path_to_check='build-src'

echo "Verifying nix code in: ${path_to_check}"

nix-linter \
    --check=DIYInherit \
    --check=EmptyInherit \
    --check=EmptyLet \
    --check=EtaReduce \
    --check=FreeLetInFunc \
    --check=LetInInheritRecset \
    --check=ListLiteralConcat \
    --check=NegateAtom \
    --check=SequentialLet \
    --check=SetLiteralUpdate \
    --check=UnfortunateArgName \
    --check=UnneededRec \
    --check=UnusedArg \
    --check=UnusedLetBind \
    --check=UpdateEmptySet \
    --check=AlphabeticalArgs \
    --check=BetaReduction \
    --check=EmptyVariadicParamSet \
    --check=UnneededAntiquote \
    --recursive \
  "${path_to_check}"

echo "${name} succeeded!" > "${out}"
