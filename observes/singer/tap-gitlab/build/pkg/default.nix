{
  lib,
  metadata,
  python_pkgs,
  src,
}: let
  runtime_deps = with python_pkgs; [
    aioextensions
    aiohttp
    asgiref
    boto3
    cachetools
    click
    more-itertools
    python-dateutil
    pytz
    requests
    legacy-paginator
    legacy-postgres-client
    legacy-singer-io
    types-requests
  ];
  dev_deps = with python_pkgs; [
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
