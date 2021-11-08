{ makePythonPypiEnvironment
, inputs
, ...
}:
makePythonPypiEnvironment {
  name = "observes-env-target-redshift-runtime-python";
  searchPathsRuntime.bin = [
    inputs.nixpkgs.gcc
    inputs.nixpkgs.postgresql
  ];
  searchPathsBuild.bin = [
    inputs.nixpkgs.gcc
    inputs.nixpkgs.postgresql
  ];
  sourcesYaml = ./pypi-sources.yaml;
}
