attrs @ {
  pkgsSkims,
  ...
}:

let
  config = import ../../../makes/skims/config attrs.copy;
  makeDerivation = import ../../../makes/utils/make-derivation pkgsSkims;
in
  makeDerivation {
    builder = ./builder.sh;
    buildInputs = config.osRequirements.runtime;
    envBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    envPythonRequirementsDevelopment = config.pythonRequirements.development;
    envPythonRequirementsRuntime = config.pythonRequirements.runtime;
    envSrcSkimsSkims = ../../../skims/skims;
    name = "skims-structure";
  }
