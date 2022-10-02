# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  __nixpkgs__,
  makeScript,
  projectPath,
  ...
}: let
  makesSrc = (import (projectPath "/makes.lock.nix")).makesSrc;

  __argSettingsBlack__ = "${makesSrc}/src/evaluator/modules/format-python/settings-black.toml";
  __argSettingsISort__ = "${makesSrc}/src/evaluator/modules/format-python/settings-isort.toml";
in
  assert builtins.pathExists __argSettingsBlack__;
  assert builtins.pathExists __argSettingsISort__;
    makeScript {
      name = "common-dev-env-fmt";
      aliases = ["universe-fmt"];
      entrypoint = ./entrypoint.sh;
      replace = {
        inherit __argSettingsBlack__;
        inherit __argSettingsISort__;
        __argPrettierPluginToml__ = __nixpkgs__.nodePackages.prettier-plugin-toml;
      };
      searchPaths.bin = [
        __nixpkgs__.black
        __nixpkgs__.isort
        __nixpkgs__.jq
        __nixpkgs__.nodePackages.prettier
        __nixpkgs__.terraform
        __nixpkgs__.shfmt
      ];
    }
