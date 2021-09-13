{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
  };
  name = "integrates-front";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
    ];
    envSources = [ packages.integrates.front.config.dev-runtime-env ];
  };
  template = path "/makes/applications/integrates/front/entrypoint.sh";
}
