{
  lib,
  pythonPkgs,
  src,
  metadata,
}: let
  runtime_deps = with pythonPkgs; [
    returns
    fa-purity
  ];
  dev_deps = [
    pythonPkgs.poetry
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
