{ nixpkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envExternalC3 = nixpkgs.fetchzip {
      url = "https://github.com/c3js/c3/archive/v0.7.18.zip";
      sha256 = "Wqfm34pE2NDMu1JMwBAR/1jcZZlVBfxRKGp/YPNlocU=";
    };
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
    envIntegratesBackAppTemplates = path "/integrates/back/src/app/templates/static";
    envIntegratesFront = path "/integrates/front";
  };
  builder = path "/makes/packages/integrates/front/build/builder.sh";
  name = "integrates-front-build";
  searchPaths = {
    envPaths = [
      nixpkgs.patch
    ];
    envSources = [ packages.integrates.front.config.dev-runtime-env ];
  };
}
