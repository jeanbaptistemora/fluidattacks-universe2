{
  lib,
  python_pkgs,
  src,
  metadata,
}: let
  runtime_deps = with python_pkgs; [
    mlxtend
    pandas
    psycopg2
  ];
  dev_deps = with python_pkgs; [
    mypy
    poetry
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
