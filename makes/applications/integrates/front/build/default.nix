{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
  };
  name = "integrates-front-build";
  searchPaths = {
    envPaths = [
      integratesPkgs.nodejs
      integratesPkgs.patch
    ];
  };
  template = path "/makes/applications/integrates/front/build/entrypoint.sh";
}
