{ nixpkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
    envSrcIntegratesFront = path "/integrates/front";
  };
  builder = path "/makes/packages/integrates/front/test/builder.sh";
  name = "integrates-front-test";
  searchPaths = {
    envPaths = [
      nixpkgs.bash
      nixpkgs.nodejs
    ];
    envSources = [ packages.integrates.front.config.dev-runtime-env ];
  };
}
