{ buildNodeRequirements
, makes
, nixpkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
let
  nodeRequirements = buildNodeRequirements {
    name = "integrates-mobile-e2e-npm";
    node = nixpkgs.nodejs-12_x;
    requirements = {
      direct = [
        "appium@1.16.0"
      ];
      inherited = [
        "fsevents@2.3.2"
      ];
    };
  };
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "integrates-mobile-e2e-pypi";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeEntrypoint {
  arguments = {
    envAndroidSdk = (nixpkgs.androidenv.composeAndroidPackages {
      abiVersions = [ "x86" "x86_64" ];
      platformVersions = [ "29" ];
    }).androidsdk;
    envApkUrl = "https://d1ahtucjixef4r.cloudfront.net/Exponent-2.18.7.apk";
    envIntegratesMobileE2eNpm = nodeRequirements;
    envJava = nixpkgs.openjdk8_headless;
  };
  name = "integrates-mobile-e2e";
  searchPaths = {
    envPaths = [
      nixpkgs.curl
      nixpkgs.nodejs-12_x
      nixpkgs.openjdk8_headless
      nixpkgs.python37
      packages.makes.kill-port
      packages.makes.wait
      pythonRequirements
    ];
    envPython37Paths = [
      pythonRequirements
    ];
  };
  template = path "/makes/applications/integrates/mobile/e2e/entrypoint.sh";
}
