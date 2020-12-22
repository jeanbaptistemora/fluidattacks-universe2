attrs @ {
  pkgsSkims,
  ...
}:

let
  config = import ../../../makes/skims/config.nix attrs.copy;
  makeDerivation = import ../../../makes/utils/make-derivation pkgsSkims;
in
  makeDerivation {
    builder = ./builder.sh;
    envBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    envPythonRequirementsDevelopment = config.pythonRequirements.development;
    envPythonRequirementsRuntime = config.pythonRequirements.runtime;
    envSrcSkimsSkims = ../../../skims/skims;
    name = "skims-security";
  }
