{ packages
, path
, skimsPkgs
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/skims/structure/builder.sh";
  envSetupSkimsDevelopment = packages.skims.config-development;
  envSetupSkimsRuntime = packages.skims.config-runtime;
  envSrcSkimsSkims = path "/skims/skims";
  name = "skims-structure";
}
