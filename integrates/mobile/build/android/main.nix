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
    __argAndroidSdk__ =
      (inputs.nixpkgs.androidenv.composeAndroidPackages {
        buildToolsVersions = ["30.0.3"];
        platformVersions = ["30"];
      })
      .androidsdk;
    __argJava__ = inputs.nixpkgs.openjdk8_headless;
    __argSecretsProd__ = projectPath "/integrates/secrets/production.yaml";
    __argSetupIntegratesMobileDevRuntime__ =
      outputs."/integrates/mobile/config/dev-runtime";
  };
  name = "integrates-mobile-build-android";
  searchPaths = {
    bin = [
      inputs.nixpkgs.git
      inputs.nixpkgs.gnused
      inputs.nixpkgs.nodejs-14_x
      inputs.nixpkgs.openjdk8_headless
    ];
    source = [
      libGit
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
      outputs."/common/utils/sops"
      outputs."/integrates/mobile/config/dev-runtime-env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
