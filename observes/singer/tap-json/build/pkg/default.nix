{
  lib,
  metadata,
  python_pkgs,
  src,
}: let
  runtime_deps = with python_pkgs; [
    click
    dateutils
    fa-purity
    pathos
    utils-logger
  ];
  build_deps = with python_pkgs; [flit-core];
  test_deps = with python_pkgs; [
    arch-lint
    mypy
    pylint
    pytest
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
  env.dev = build_env (runtime_deps ++ test_deps);
  env.bin = build_env [pkg];
}
