{ makeScript
, outputs
, ...
}:
makeScript {
  name = "integrates-front-deploy-prod";
  searchPaths.source = [ outputs."/integrates/front/deploy" ];
  entrypoint = ./entrypoint.sh;
}
