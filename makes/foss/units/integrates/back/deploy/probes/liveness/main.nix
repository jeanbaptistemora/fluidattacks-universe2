{ makeScript
, outputs
, ...
}:
makeScript {
  name = "integrates-back-deploy-probes-liveness";
  searchPaths = {
    source = [
      outputs."/utils/aws"
      outputs."/integrates/back/deploy/probes/lib"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
