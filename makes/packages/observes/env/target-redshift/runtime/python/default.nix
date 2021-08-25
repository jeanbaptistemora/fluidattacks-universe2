{ makes
, nixpkgs
, ...
}:
makes.makePythonPypiEnvironment {
  name = "observes-env-target-redshift-runtime-python";
  searchPaths.bin = [ nixpkgs.gcc nixpkgs.postgresql ];
  sourcesYaml = ./pypi-sources.yaml;
}
