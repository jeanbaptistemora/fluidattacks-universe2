{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "integrates-front-deploy-prod";
  arguments = {
    envCompiledFront = packages.integrates.front.build-pkg.prod;
  };
  searchPaths = {
    envSources = [
      packages.integrates.front.deploy-pkg
    ];
  };
  template = path "/makes/applications/integrates/front/deploy/prod/entrypoint.sh";
}
