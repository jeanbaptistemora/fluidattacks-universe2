{ inputs
, makeScript
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
    inputs.product.makes-kill-port
    inputs.product.makes-wait
  ];
  entrypoint = ./entrypoint.sh;
}
