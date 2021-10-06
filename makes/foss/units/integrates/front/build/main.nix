{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  env = {
    envExternalC3 = inputs.nixpkgs.fetchzip {
      url = "https://github.com/c3js/c3/archive/v0.7.18.zip";
      sha256 = "Wqfm34pE2NDMu1JMwBAR/1jcZZlVBfxRKGp/YPNlocU=";
    };
    envSetupIntegratesFrontDevRuntime =
      outputs."/integrates/front/config/dev-runtime";
    envIntegratesBackAppTemplates = projectPath "/integrates/back/src/app/templates/static";
    envIntegratesFront = projectPath "/integrates/front";
  };
  builder = projectPath "/makes/foss/units/integrates/front/build/builder.sh";
  name = "integrates-front-build";
  searchPaths = {
    bin = [ inputs.nixpkgs.patch ];
    source = [ outputs."/integrates/front/config/dev-runtime-env" ];
  };
}
