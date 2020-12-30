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
    envSrcSkimsProspectorProfile = ../../../skims/.prospector.yaml;
    envSrcSkimsSettingsCfg = ../../../skims/settings.cfg;
    envSrcSkimsSkims = ../../../skims/skims;
    envSrcSkimsTest = ../../../skims/test;
    name = "skims-lint";
  }
