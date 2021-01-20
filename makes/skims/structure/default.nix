{ path
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/skims/structure/builder.sh";
  envSetupSkimsDevelopment = config.setupSkimsDevelopment;
  envSetupSkimsRuntime = config.setupSkimsRuntime;
  envSrcSkimsSkims = path "/skims/skims";
  name = "skims-structure";
}
