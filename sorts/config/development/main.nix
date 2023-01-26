{
  inputs,
  makeTemplate,
  makePythonPypiEnvironment,
  projectPath,
  ...
}: let
  pythonRequirements = makePythonPypiEnvironment {
    name = "sorts-development";
    searchPathsRuntime.bin = [
      inputs.nixpkgs.gcc
      inputs.nixpkgs.postgresql
    ];
    searchPathsBuild.bin = [
      inputs.nixpkgs.gcc
      inputs.nixpkgs.postgresql
    ];
    sourcesYaml = ./pypi-sources.yaml;

    # Required when using psycopg2 on Python3.8
    # Can be removed once we upgrade to Python3.9
    searchPathsBuild.export = [["CPATH" inputs.nixpkgs.libxcrypt "/include"]];
  };
in
  makeTemplate {
    name = "sorts-config-development";
    searchPaths = {
      rpath = [
        inputs.nixpkgs.gcc.cc.lib
      ];
      pythonPackage = [
        (projectPath "/sorts/training")
      ];
      source = [pythonRequirements];
    };
  }
