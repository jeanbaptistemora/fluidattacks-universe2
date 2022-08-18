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
    pathos
    python-dateutil
    mypy-boto3-s3
    types-boto3
    types-dateutil
    utils-logger
  ];
  build_deps = with python_pkgs; [flit-core];
  test_deps = with python_pkgs; [
    arch-lint
    mypy
    pytest
    pytest-timeout
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
