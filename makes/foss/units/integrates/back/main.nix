{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argCertsDevelopment__ = inputs.product.integrates-back-certs-development;
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-back";
  searchPaths.bin = [
    inputs.product.makes-done
    inputs.product.makes-kill-port
    inputs.product.makes-wait
  ];
  entrypoint = ./entrypoint.sh;
}
