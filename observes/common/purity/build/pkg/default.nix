# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  python_pkgs,
  src,
  metadata,
}: let
  runtime_deps = with python_pkgs; [
    returns
    fa-purity
  ];
  build_deps = with python_pkgs; [poetry-core];
  test_deps = [];
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
  env.build = build_env (runtime_deps ++ test_deps ++ build_deps);
  env.bin = build_env [pkg];
}
