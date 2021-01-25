{ path
, skimsPkgs
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/skims/docs/build/builder.sh";
  envBashLibPython = path "/makes/utils/python/template.sh";
  envSetupSkimsDevelopment = import (path "/makes/packages/skims/config-development") attrs.copy;
  envSetupSkimsRuntime = import (path "/makes/packages/skims/config-runtime") attrs.copy;
  envSrcSkimsDocs = path "/skims/docs";
  envSrcSkimsReadme = path "/skims/README.md";
  envSrcSkimsSkims = path "/skims/skims";
  name = "skims-docs-build";
}
