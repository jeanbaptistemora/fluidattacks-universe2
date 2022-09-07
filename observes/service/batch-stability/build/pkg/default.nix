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
    boto3
    bugsnag
    click
    fa-purity
    mypy-boto3-batch
    utils-logger
    types-click
    types-boto3
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
