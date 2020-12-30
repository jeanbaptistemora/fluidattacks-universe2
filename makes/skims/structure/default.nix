attrs @ {
  skimsPkgs,
  ...
}:

let
  config = import ../../../makes/skims/config attrs.copy;
  makeDerivation = import ../../../makes/utils/make-derivation skimsPkgs;
in
  makeDerivation {
    builder = ./builder.sh;
    envSetupSkimsDevelopment = config.setupSkimsDevelopment;
    envSetupSkimsRuntime = config.setupSkimsRuntime;
    envSrcSkimsSkims = ../../../skims/skims;
    name = "skims-structure";
  }
