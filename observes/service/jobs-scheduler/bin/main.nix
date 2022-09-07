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
  root = projectPath inputs.observesIndex.service.scheduler.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeScript {
    name = "observes-scheduler";
    searchPaths = {
      bin = [
        env
      ];
      source = [
        outputs."${inputs.observesIndex.service.scheduler.env.runtime}"
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
