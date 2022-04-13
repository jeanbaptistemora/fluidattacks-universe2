{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-back-deploy-probes-readiness";
  searchPaths.source = [
    outputs."/common/utils/aws"
    outputs."/integrates/back/deploy/probes/lib"
  ];
  entrypoint = ./entrypoint.sh;
}
