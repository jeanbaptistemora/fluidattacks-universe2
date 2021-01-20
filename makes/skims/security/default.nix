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
  envSetupSkimsDevelopment = config.setupSkimsDevelopment;
  envSrcSkimsSkims = (path "/skims/skims");
  name = "skims-security";
}
