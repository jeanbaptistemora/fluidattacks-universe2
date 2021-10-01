{ inputs
, makeScript
, projectPath
, ...
}:
makeScript {
  replace = {
    __argSecretsDev__ = projectPath "/integrates/secrets-development.yaml";
    __argSetupIntegratesMobileDevRuntime__ =
      inputs.product.integrates-mobile-config-dev-runtime;
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
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
      inputs.product.integrates-mobile-config-dev-runtime-env
    ];
  };
  entrypoint = ./entrypoint.sh;
}
