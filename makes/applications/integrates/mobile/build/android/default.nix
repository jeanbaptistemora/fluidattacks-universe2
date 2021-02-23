{ integratesMobilePkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint integratesMobilePkgs {
  arguments = {
    envAndroidSdk = (integratesMobilePkgs.androidenv.composeAndroidPackages {
      buildToolsVersions = [ "29.0.2" "30.0.3" ];
      platformVersions = [ "29" ];
    }).androidsdk;
    envJava = integratesMobilePkgs.openjdk8_headless;
    envSecretsProd = path "/integrates/secrets-production.yaml";
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
  };
  name = "integrates-mobile-build-android";
  searchPaths = {
    envPaths = [
      integratesMobilePkgs.git
      integratesMobilePkgs.gnused
      integratesMobilePkgs.nodejs-12_x
      integratesMobilePkgs.openjdk8_headless
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/mobile/build/android/entrypoint.sh";
}
