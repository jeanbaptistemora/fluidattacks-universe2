{ libGit
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "integrates-front-deploy-dev";
  searchPaths.source = [
    libGit
    outputs."/integrates/front/deploy"
  ];
  entrypoint = projectPath "/makes/foss/units/integrates/front/deploy/dev/entrypoint.sh";
}
