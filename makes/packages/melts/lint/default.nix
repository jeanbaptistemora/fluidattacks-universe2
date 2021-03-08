{ nixpkgs
, packages
, path
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixpkgs;
in
makeDerivation {
  arguments = {
    envSetupMeltsDevelopment = packages.melts.config-development;
    envSetupMeltsRuntime = packages.melts.config-runtime;
    envSrcMeltsToolbox = path "/melts/toolbox";
    envSrcMeltsTest = path "/melts/tests";
  };
  builder = path "/makes/packages/melts/lint/builder.sh";
  name = "melts-lint";
  searchPaths = {
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
