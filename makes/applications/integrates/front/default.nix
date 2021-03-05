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
  };
  template = path "/makes/applications/integrates/front/entrypoint.sh";
}
