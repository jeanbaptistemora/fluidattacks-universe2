{ inputs
, makeScript
, ...
}:
makeScript {
  replace = {
    __argCertsDevelopment__ = inputs.product.integrates-back-certs-development;
    __argIntegratesEnv__ = inputs.product.integrates-back-env;
  };
  name = "integrates-back";
  searchPaths.bin = [
    inputs.product.makes-done
    inputs.product.makes-kill-port
    inputs.product.makes-wait
  ];
  entrypoint = ./entrypoint.sh;
}
