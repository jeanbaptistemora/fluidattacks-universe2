{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  name = "integrates-back-deploy-probes-liveness";
  searchPaths = {
    source = [
      (inputs.legacy.importUtility "aws")
      outputs."/integrates/back/deploy/probes/lib"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
