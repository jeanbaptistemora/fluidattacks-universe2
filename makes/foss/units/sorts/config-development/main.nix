{ inputs
, makeTemplate
, makePythonPypiEnvironment
, projectPath
, ...
}:
let
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
    source = [ pythonRequirements ];
  };
}
