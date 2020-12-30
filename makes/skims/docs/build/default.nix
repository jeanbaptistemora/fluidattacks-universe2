attrs @ {
  skimsPkgs,
  ...
}:

let
  config = import ../../../../makes/skims/config attrs.copy;
  makeDerivation = import ../../../../makes/utils/make-derivation skimsPkgs;
in
  makeDerivation {
    builder = ./builder.sh;
    envBashLibPython = ../../../../makes/utils/bash-lib/python.sh;
    envContextFile = config.contextFile;
    envPythonRequirementsDevelopment = config.pythonRequirements.development;
    envPythonRequirementsRuntime = config.pythonRequirements.runtime;
    envSrcSkimsDocs = ../../../../skims/docs;
    envSrcSkimsReadme = ../../../../skims/README.md;
    envSrcSkimsSkims = ../../../../skims/skims;
    name = "skims-docs-build";
  }
