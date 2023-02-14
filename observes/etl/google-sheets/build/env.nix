{
  lib,
  pkg,
  runtime_deps,
  test_deps,
}: let
  build_env = extraLibs:
    lib.buildEnv {
      inherit extraLibs;
      ignoreCollisions = false;
    };
in {
  runtime = build_env runtime_deps;
  dev = build_env (runtime_deps ++ test_deps);
  bin = build_env [pkg];
}
