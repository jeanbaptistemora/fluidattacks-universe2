{ packages
, path
, skimsPkgs
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/skims/docs/build/builder.sh";
  envBashLibPython = path "/makes/utils/python/template.sh";
  envSetupSkimsDevelopment = packages.skims.config-development;
  envSetupSkimsRuntime = packages.skims.config-runtime;
  envSrcSkimsDocs = path "/skims/docs";
  envSrcSkimsReadme = path "/skims/README.md";
  envSrcSkimsSkims = path "/skims/skims";
  name = "skims-docs-build";
}
