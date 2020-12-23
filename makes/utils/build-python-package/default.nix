# Do a pip install of the provided package

pkgs:

{
  dependencies,
  packagePath,
  python,
}:

let
  makeDerivation = import ../../../makes/utils/make-derivation pkgs;
in
  makeDerivation {
    builder = ./builder.sh;
    buildInputs = dependencies ++ [ python ];
    envPackagePath = packagePath;
    name = "build-python-package";
  }
