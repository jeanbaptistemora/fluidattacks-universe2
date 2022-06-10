{
  lib,
  metadata,
  python_pkgs,
  src,
}: let
  runtime_deps = with python_pkgs; [
    boto3
    click
    fa-purity
    fa-singer-io
    jsonschema
    psycopg2
    returns
  ];
  build_deps = with python_pkgs; [poetry];
  test_deps = with python_pkgs; [
    import-linter
    mypy
    pytest
    toml
    types-toml
  ];
  pkg = (import ./build.nix) {
    inherit lib src metadata runtime_deps build_deps test_deps;
  };
  build_env = extraLibs:
    lib.buildEnv {
      inherit extraLibs;
      ignoreCollisions = false;
    };
in {
  inherit pkg;
  env.runtime = build_env runtime_deps;
  env.dev = build_env (runtime_deps ++ test_deps ++ build_deps);
  env.bin = build_env [pkg];
}
