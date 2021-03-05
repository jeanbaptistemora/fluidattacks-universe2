{ buildNodeRequirements
, buildPythonRequirements
, nixpkgs2
, makeEntrypoint
, packages
, path
, ...
} @ _:
let
  nodeRequirements = buildNodeRequirements {
    name = "integrates-mobile-e2e-npm";
    node = nixpkgs2.nodejs-12_x;
    requirements = {
      direct = [
        "appium@1.16.0"
      ];
      inherited = [
        "fsevents@2.3.2"
      ];
    };
  };
  pythonRequirements = buildPythonRequirements {
    name = "integrates-mobile-e2e-pypi";
    python = nixpkgs2.python37;
    requirements = {
      direct = [
        "Appium-Python-Client==1.0.2"
        "pytest==6.0.1"
      ];
      inherited = [
        "attrs==20.3.0"
        "importlib-metadata==3.6.0"
        "iniconfig==1.1.1"
        "more-itertools==8.7.0"
        "packaging==20.9"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "selenium==3.141.0"
        "toml==0.10.2"
        "typing-extensions==3.7.4.3"
        "urllib3==1.26.3"
        "zipp==3.4.0"
      ];
    };
  };
in
makeEntrypoint {
  arguments = {
    envAndroidSdk = (nixpkgs2.androidenv.composeAndroidPackages {
      abiVersions = [ "x86" "x86_64" ];
      platformVersions = [ "29" ];
    }).androidsdk;
    envApkUrl = "https://d1ahtucjixef4r.cloudfront.net/Exponent-2.18.7.apk";
    envIntegratesMobileE2eNpm = nodeRequirements;
    envJava = nixpkgs2.openjdk8_headless;
  };
  name = "integrates-mobile-e2e";
  searchPaths = {
    envPaths = [
      nixpkgs2.curl
      nixpkgs2.nodejs-12_x
      nixpkgs2.openjdk8_headless
      nixpkgs2.python37
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
