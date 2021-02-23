{ meltsPkgs
, packages
, path
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path meltsPkgs;
in
makeDerivation {
  arguments = {
    envBashLibLintPython = import (path "/makes/utils/lint-python") path meltsPkgs;
    envSetupMeltsDevelopment = packages.melts.config-development;
    envSetupMeltsRuntime = packages.melts.config-runtime;
    envSrcMeltsToolbox = path "/melts/toolbox";
    envSrcMeltsTest = path "/melts/tests";
  };
  builder = path "/makes/packages/melts/lint/builder.sh";
  name = "melts-lint";
}
