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
  name = "integrates-front-build";
  searchPaths = {
    envPaths = [
      nixpkgs2.nodejs
      nixpkgs2.patch
    ];
  };
  template = path "/makes/applications/integrates/front/build/entrypoint.sh";
}
