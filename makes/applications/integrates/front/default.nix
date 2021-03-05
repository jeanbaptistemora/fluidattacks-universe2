{ nixpkgs2
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
      nixpkgs2.nodejs
    ];
  };
  template = path "/makes/applications/integrates/front/entrypoint.sh";
}
