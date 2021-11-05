{ makeScript
, outputs
, ...
}:
makeScript {
  name = "integrates-back-authz-matrix";
  replace.__argIntegratesBackEnv__ = outputs."/integrates/back/env";
  entrypoint = ./entrypoint.sh;
}
