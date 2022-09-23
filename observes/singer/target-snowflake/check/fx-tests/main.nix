# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fetchNixpkgs,
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.target.snowflake.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeScript {
    name = "target-snowflake";
    replace = {
      __argSecrets__ = projectPath "/observes/secrets/prod.yaml";
      __argFxTests__ = "${root}/fx_tests";
    };
    searchPaths = {
      bin = [
        env
      ];
      source = [
        (outputs."/common/utils/sops")
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
