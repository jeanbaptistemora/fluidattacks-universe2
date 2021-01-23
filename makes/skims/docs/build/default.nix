{ path
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/skims/docs/build/builder.sh";
  envBashLibPython = path "/makes/utils/python.sh";
  envSetupSkimsDevelopment = config.setupSkimsDevelopment;
  envSetupSkimsRuntime = config.setupSkimsRuntime;
  envSrcSkimsDocs = path "/skims/docs";
  envSrcSkimsReadme = path "/skims/README.md";
  envSrcSkimsSkims = path "/skims/skims";
  name = "skims-docs-build";
}
