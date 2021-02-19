{ packages
, path
, skimsPkgs
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  arguments = {
    envSetupSkimsDevelopment = packages.skims.config-development;
    envSrcSkimsSkims = path "/skims/skims";
  };
  builder = path "/makes/packages/skims/security/builder.sh";
  name = "skims-security";
}
