{ libGit
, makeScript
, outputs
, ...
}:
makeScript {
  name = "integrates-front-deploy-dev";
  searchPaths.source = [
    libGit
    outputs."/integrates/front/deploy"
  ];
  entrypoint = ./entrypoint.sh;
}
