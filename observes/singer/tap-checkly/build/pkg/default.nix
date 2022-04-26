{
  lib,
  pythonPkgs,
  src,
  metadata,
}: let
  runtime_deps = with pythonPkgs; [
    click
    fa-purity
    fa-singer-io
    legacy-purity
    legacy-paginator
    legacy-singer-io
    python-dateutil
    requests
    types-click
    types-python-dateutil
    types-requests
    utils-logger
  ];
  dev_deps = with pythonPkgs; [
    import-linter
    mypy
    poetry
    pytest
    toml
    types-toml
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
