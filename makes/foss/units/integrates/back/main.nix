{ makeScript
, outputs
, managePorts
, ...
}:
makeScript {
  replace = {
    __argCertsDevelopment__ = outputs."/integrates/back/certs/dev";
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-back";
  searchPaths.source = [
    managePorts
  ];
  entrypoint = ./entrypoint.sh;
}
