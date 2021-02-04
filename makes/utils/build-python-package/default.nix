# Do a pip install of the provided package

path: pkgs:

{ dependencies
, name
, packagePath
, python
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
in
makeDerivation {
  builder = path "/makes/utils/build-python-package/builder.sh";
  buildInputs = dependencies ++ [ python ];
  envPackagePath = packagePath;
  name = "build-python-package-${name}";
}
