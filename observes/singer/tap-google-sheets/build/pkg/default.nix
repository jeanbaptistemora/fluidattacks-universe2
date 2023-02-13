{
  lib,
  metadata,
  python_pkgs,
}: let
  runtime_deps = with python_pkgs; [
    backoff
    requests
    singer-python
  ];
  src = lib.fetchPypi {
    inherit (metadata) version;
    pname = metadata.name;
    sha256 = "4rOc+V71H2XjEOIOjeamoa9poReLYCEcu+k8hYOoDQI=";
  };
  pkg = (import ./build.nix) {
    inherit lib src metadata runtime_deps;
  };
  build_env = extraLibs:
    lib.buildEnv {
      inherit extraLibs;
      ignoreCollisions = false;
    };
in {
  inherit pkg;
  env.runtime = build_env runtime_deps;
  env.dev = build_env runtime_deps;
  env.bin = build_env [pkg];
}
