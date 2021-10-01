{ makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "integrates-front-deploy-prod";
  searchPaths.source = [ outputs."/integrates/front/deploy" ];
  entrypoint = projectPath "/makes/foss/units/integrates/front/deploy/prod/entrypoint.sh";
}
