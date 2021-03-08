{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "integrates-front-deploy-prod";
  searchPaths = {
    envSources = [
      packages.integrates.front.deploy
    ];
  };
  template = path "/makes/applications/integrates/front/deploy/prod/entrypoint.sh";
}
