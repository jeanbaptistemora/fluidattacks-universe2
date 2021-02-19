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
  arguments = {
    envPackagePath = packagePath;
  };
  builder = path "/makes/utils/build-python-package/builder.sh";
  name = "build-python-package-${name}";
  searchPaths = {
    envPaths = dependencies ++ [ python ];
  };
}
