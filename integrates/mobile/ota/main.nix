{
  inputs,
  libGit,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
    __argSecretsProd__ = projectPath "/integrates/secrets/production.yaml";
    __argSetupIntegratesMobileDevRuntime__ =
      outputs."/integrates/mobile/config/dev-runtime";
  };
  name = "integrates-mobile-ota";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnused
      inputs.nixpkgs.nodejs-12_x
      inputs.nixpkgs.openssl
      outputs."/common/utils/bugsnag/announce"
    ];
    source = [
      libGit
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/integrates/mobile/config/dev-runtime-env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
