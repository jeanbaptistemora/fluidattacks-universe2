{ makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argCertsDevelopment__ = outputs."/integrates/back/certs/dev";
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-back";
  searchPaths.bin = [
    outputs."/makes/done"
    outputs."/makes/kill-port"
    outputs."/makes/wait"
  ];
  entrypoint = ./entrypoint.sh;
}
