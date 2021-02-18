{ packages
, path
, skimsPkgs
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/skims/security/builder.sh";
  envSetupSkimsDevelopment = packages.skims.config-development;
  envSrcSkimsSkims = path "/skims/skims";
  name = "skims-security";
}
