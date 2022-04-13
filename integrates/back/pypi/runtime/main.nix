{
  makeTemplate,
  makePythonPypiEnvironment,
  outputs,
  projectPath,
  inputs,
  ...
}: let
  self_bugsnag = inputs.nixpkgs.python39Packages.bugsnag.overridePythonAttrs (_: rec {
    src =
      builtins.fetchGit
      {
        url = "https://github.com/fluidattacks/bugsnag-python";
        ref = "master";
        rev = "41387bcff4ae94ae633725889cb55567bcce5c9e";
      };
    doCheck = false;
  });
  pythonRequirements = makePythonPypiEnvironment {
    name = "integrates-back-runtime";
    sourcesYaml = ./pypi-sources.yaml;
    searchPathsBuild = {
      bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
    };
    searchPathsRuntime = {
      bin = [
        inputs.nixpkgs.gcc
        inputs.nixpkgs.postgresql
        inputs.nixpkgs.gnutar
        inputs.nixpkgs.gzip
      ];
    };
    withSetuptools_57_4_0 = true;
    withWheel_0_37_0 = true;
  };
in
  makeTemplate {
    name = "integrates-back-pypi-runtime";
    searchPaths = {
      pythonPackage = [
        "${self_bugsnag}/lib/python3.9/site-packages/"
        (projectPath "/integrates/back/src")
        (projectPath "/integrates")
        (projectPath "/common/utils/bugsnag/client")
      ];
      source = [
        pythonRequirements
        outputs."/common/python/safe-pickle"
      ];
    };
  }
