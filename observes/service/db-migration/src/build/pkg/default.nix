# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  pythonPkgs,
  src,
  metadata,
}: let
  runtime_deps = [
    pythonPkgs.redshift-client
    pythonPkgs.utils-logger
  ];
  dev_deps = [
    pythonPkgs.mypy
    pythonPkgs.pytest
    pythonPkgs.toml
    pythonPkgs.types-toml
  ];
  build_pkg = propagatedBuildInputs:
    (import ./build.nix) {
      nativeBuildInputs = [pythonPkgs.poetry] ++ dev_deps;
      inherit lib src metadata propagatedBuildInputs;
    };
in {
  runtime = build_pkg runtime_deps;
  dev = build_pkg (runtime_deps ++ dev_deps);
}
