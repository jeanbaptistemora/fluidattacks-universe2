{
  lib,
  pythonPkgs,
  src,
  metadata,
}: let
  runtime_deps = [
    pythonPkgs.click
    pythonPkgs.fa-purity
    pythonPkgs.GitPython
    pythonPkgs.pathos
    pythonPkgs.postgres-client
    pythonPkgs.psycopg2
    pythonPkgs.ratelimiter
    pythonPkgs.redshift-client
    pythonPkgs.requests
    pythonPkgs.six
    pythonPkgs.types-click
    pythonPkgs.types-requests
    pythonPkgs.utils-logger
  ];
  dev_deps = [
    pythonPkgs.import-linter
    pythonPkgs.mypy
    pythonPkgs.poetry
    pythonPkgs.pytest
    pythonPkgs.toml
    pythonPkgs.types-toml
  ];
  pkg = (import ./build.nix) {
    inherit lib src metadata;
    nativeBuildInputs = dev_deps;
    propagatedBuildInputs = runtime_deps;
  };
  build_env = extraLibs:
    lib.buildEnv {
      inherit extraLibs;
      ignoreCollisions = false;
    };
in {
  inherit pkg;
  env.runtime = build_env runtime_deps;
  env.dev = build_env (runtime_deps ++ dev_deps);
  env.bin = build_env [pkg];
}
