{
  inputs,
  makeNodeJsModules,
  makePythonPypiEnvironment,
  makeScript,
  managePorts,
  ...
} @ _: let
  nodeJsModules = makeNodeJsModules {
    name = "integrates-mobile-e2e-npm";
    nodeJsVersion = "14";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };

  pythonRequirements = makePythonPypiEnvironment {
    name = "integrates-mobile-e2e-pypi";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
  makeScript {
    replace = {
      __argAndroidSdk__ =
        (inputs.nixpkgs.androidenv.composeAndroidPackages {
          abiVersions = ["x86" "x86_64"];
          platformVersions = ["29"];
        })
        .androidsdk;
      __argApkUrl__ = "https://d1ahtucjixef4r.cloudfront.net/Exponent-2.18.7.apk";
      __argIntegratesMobileE2eNpm__ = nodeJsModules;
      __argJava__ = inputs.nixpkgs.openjdk8_headless;
    };
    name = "integrates-mobile-e2e";
    searchPaths = {
      bin = [
        inputs.nixpkgs.curl
        inputs.nixpkgs.nodejs-14_x
        inputs.nixpkgs.openjdk8_headless
        inputs.nixpkgs.python39
      ];
      nodeModule = ["."];
      source = [
        managePorts
        pythonRequirements
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
