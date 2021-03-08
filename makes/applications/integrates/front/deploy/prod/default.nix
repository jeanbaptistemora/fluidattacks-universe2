{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "integrates-front-deploy-prod";
  arguments = {
    envCompiledFront = packages.integrates.front.build.prod;
  };
  searchPaths = {
    envSources = [
      packages.integrates.front.deploy
    ];
  };
  template = path "/makes/applications/integrates/front/deploy/prod/entrypoint.sh";
}
