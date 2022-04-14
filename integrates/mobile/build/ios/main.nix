{
  inputs,
  libGit,
  makeScript,
  outputs,
  projectPath,
  ...
} @ _:
makeScript {
  replace = {
    __argSecretsProd__ = projectPath "/integrates/secrets/production.yaml";
    __argIntegratesMobileDevRuntime__ =
      outputs."/integrates/mobile/config/dev-runtime";
  };
  name = "integrates-mobile-build-ios";
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.nodejs-12_x
    ];
    source = [
      libGit
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/integrates/mobile/config/dev-runtime-env"
    ];
  };
  entrypoint = projectPath "/integrates/mobile/build/ios/entrypoint.sh";
}
