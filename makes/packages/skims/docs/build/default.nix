{ packages
, path
, skimsPkgs
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  arguments = {
    envBashLibPython = path "/makes/utils/python/template.sh";
    envSetupSkimsDevelopment = packages.skims.config-development;
    envSetupSkimsRuntime = packages.skims.config-runtime;
    envSrcSkimsDocs = path "/skims/docs";
    envSrcSkimsReadme = path "/skims/README.md";
    envSrcSkimsSkims = path "/skims/skims";
  };
  builder = path "/makes/packages/skims/docs/build/builder.sh";
  name = "skims-docs-build";
}
