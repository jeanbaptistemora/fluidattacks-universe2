{ nixPkgs
, observesPackage
, path
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixPkgs;
in
makeDerivation {
  arguments = {
    envSrc = observesPackage.packagePath;
  };
  builder = path "/makes/libs/observes/linter/builder.sh";
  name = "observes-linter-${observesPackage.name}";
  searchPaths = {
    envPaths = observesPackage.buildInputs ++ [ nixPkgs.findutils ];
    envSources = [ observesPackage.template ];
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
