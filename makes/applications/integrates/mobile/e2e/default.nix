{ makes
, nixpkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
let
  nodeJsModules = makes.makeNodeJsModules {
    name = "integrates-mobile-e2e-npm";
    nodeJsVersion = "12";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
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
    envIntegratesMobileE2eNpm = nodeJsModules;
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
    ];
    envNodeLibraries = [ "." ];
    envSources = [
      pythonRequirements
    ];
  };
  template = path "/makes/applications/integrates/mobile/e2e/entrypoint.sh";
}
