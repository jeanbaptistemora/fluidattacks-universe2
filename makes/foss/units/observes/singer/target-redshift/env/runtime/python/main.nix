{ makePythonPypiEnvironment
, inputs
, ...
}:
makePythonPypiEnvironment {
  name = "observes-singer-target-redshift-env-runtime-python";
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
