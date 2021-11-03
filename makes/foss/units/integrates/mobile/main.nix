{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  replace = {
    __argSecretsDev__ = projectPath "/integrates/secrets-development.yaml";
    __argSetupIntegratesMobileDevRuntime__ =
      outputs."/integrates/mobile/config/dev-runtime";
  };
  name = "integrates-mobile";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.iproute
      inputs.nixpkgs.nodejs-12_x
      inputs.nixpkgs.xdg_utils
    ];
    source = [
      (outputs."/utils/aws")
      (outputs."/utils/sops")
      outputs."/integrates/mobile/config/dev-runtime-env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
