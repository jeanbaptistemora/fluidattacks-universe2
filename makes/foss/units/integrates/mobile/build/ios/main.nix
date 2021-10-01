{ inputs
, libGit
, makeScript
, projectPath
, ...
} @ _:
makeScript {
  replace = {
    __argSecretsProd__ = projectPath "/integrates/secrets-production.yaml";
    __argIntegratesMobileDevRuntime__ = inputs.product.integrates-mobile-config-dev-runtime;
  };
  name = "integrates-mobile-build-ios";
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.nodejs-12_x
    ];
    source = [
      libGit
      inputs.product.integrates-mobile-config-dev-runtime-env
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/mobile/build/ios/entrypoint.sh";
}
