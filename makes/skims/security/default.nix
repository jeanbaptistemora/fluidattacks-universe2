{ path
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/skims/security/builder.sh";
  envSetupSkimsDevelopment = config.setupSkimsDevelopment;
  envSrcSkimsSkims = path "/skims/skims";
  name = "skims-security";
}
