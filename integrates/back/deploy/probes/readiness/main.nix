{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-back-deploy-probes-readiness";
  searchPaths.source = [
    outputs."/integrates/back/deploy/probes/lib"
  ];
  entrypoint = ./entrypoint.sh;
}
