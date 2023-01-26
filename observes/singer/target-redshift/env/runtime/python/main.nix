{
  makePythonPypiEnvironment,
  inputs,
  ...
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

  # Required when using psycopg2 on Python3.8
  # Can be removed once we upgrade to Python3.9
  searchPathsBuild.export = [["CPATH" inputs.nixpkgs.libxcrypt "/include"]];
}
