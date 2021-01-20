{ path
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") skimsPkgs;
in
makeDerivation {
  builder = ./builder.sh;
  envBashLibPython = (path "/makes/utils/bash-lib/python.sh");
  envSetupSkimsDevelopment = config.setupSkimsDevelopment;
  envSetupSkimsRuntime = config.setupSkimsRuntime;
  envSrcSkimsDocs = (path "/skims/docs");
  envSrcSkimsReadme = (path "/skims/README.md");
  envSrcSkimsSkims = (path "/skims/skims");
  name = "skims-docs-build";
}
