{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint integratesPkgs {
  arguments = {
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
  };
  name = "integrates-front";
  searchPaths = {
    envPaths = [
      integratesPkgs.nodejs
    ];
  };
  template = path "/makes/applications/integrates/front/entrypoint.sh";
}
