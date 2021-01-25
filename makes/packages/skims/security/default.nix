{ path
, skimsPkgs
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/skims/security/builder.sh";
  envSetupSkimsDevelopment = import (path "/makes/packages/skims/config-development") attrs.copy;
  envSrcSkimsSkims = path "/skims/skims";
  name = "skims-security";
}
