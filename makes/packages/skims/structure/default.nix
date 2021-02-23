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
    envSetupSkimsDevelopment = packages.skims.config-development;
    envSetupSkimsRuntime = packages.skims.config-runtime;
    envSrcSkimsSkims = path "/skims/skims";
  };
  builder = path "/makes/packages/skims/structure/builder.sh";
  name = "skims-structure";
}
