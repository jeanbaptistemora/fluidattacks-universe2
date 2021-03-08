{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "integrates-front-deploy-dev";
  arguments = {
    envCompiledFront = packages.integrates.front.build-pkg.dev;
  };
  searchPaths = {
    envSources = [
      packages.integrates.front.deploy-pkg
    ];
  };
  template = path "/makes/applications/integrates/front/deploy/dev/entrypoint.sh";
}
