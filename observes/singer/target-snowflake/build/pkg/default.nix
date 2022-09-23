# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  metadata,
  python_pkgs,
  src,
}: let
  runtime_deps = with python_pkgs; [
    click
    fa-purity
    fa-singer-io
    jsonschema
    pathos
    snowflake-connector-python
    utils-logger
  ];
  build_deps = with python_pkgs; [flit-core];
  test_deps = with python_pkgs; [
    arch-lint
    mypy
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
  env.dev = build_env (runtime_deps ++ test_deps ++ build_deps);
  env.bin = build_env [pkg];
}
