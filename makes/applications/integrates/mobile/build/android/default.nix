{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAndroidSdk = (nixpkgs.androidenv.composeAndroidPackages {
      buildToolsVersions = [ "30.0.3" ];
      platformVersions = [ "30" ];
    }).androidsdk;
    envJava = nixpkgs.openjdk8_headless;
    envSecretsProd = path "/integrates/secrets-production.yaml";
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
  };
  name = "integrates-mobile-build-android";
  searchPaths = {
    envPaths = [
      nixpkgs.git
      nixpkgs.gnused
      nixpkgs.nodejs-12_x
      nixpkgs.openjdk8_headless
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
    envSources = [ packages.integrates.mobile.config.dev-runtime-env ];
  };
  template = path "/makes/applications/integrates/mobile/build/android/entrypoint.sh";
}
