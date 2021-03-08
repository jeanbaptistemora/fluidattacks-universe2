{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAndroidSdk = (nixpkgs.androidenv.composeAndroidPackages {
      buildToolsVersions = [ "29.0.2" "30.0.3" ];
      platformVersions = [ "29" ];
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
  };
  template = path "/makes/applications/integrates/mobile/build/android/entrypoint.sh";
}
