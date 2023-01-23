{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  ...
}: let
  pythonRequirements = makePythonPypiEnvironment {
    name = "integrates-streams-runtime";
    sourcesYaml = ./pypi-sources.yaml;
    searchPathsBuild = {
      bin = [
        inputs.nixpkgs.gcc
        inputs.nixpkgs.postgresql
      ];
    };
    searchPathsRuntime = {
      bin = [
        inputs.nixpkgs.gcc
        inputs.nixpkgs.postgresql
      ];
    };
  };
  amazon_kclpy = outputs."/integrates/streams/runtime/amazon_kclpy";
  amazon_kclpy_package = "${amazon_kclpy}/lib/python3.11/site-packages";
in
  makeTemplate {
    name = "integrates-streams-runtime";
    searchPaths = {
      pythonPackage = [
        amazon_kclpy_package
      ];
      source = [
        pythonRequirements
      ];
    };
    template = ''
      export CLASSPATH="${amazon_kclpy_package}/amazon_kclpy/jars/*"
    '';
  }
