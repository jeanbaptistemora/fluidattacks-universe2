{ makePythonPypiEnvironment
, inputs
, ...
}:
makePythonPypiEnvironment {
  name = "observes-env-target-redshift-runtime-python";
  searchPaths.bin = [
    inputs.nixpkgs.gcc
    inputs.nixpkgs.postgresql
  ];
  sourcesYaml = ./pypi-sources.yaml;
}
