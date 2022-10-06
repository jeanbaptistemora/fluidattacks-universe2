# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.checkly.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath fetchNixpkgs;
    observesIndex = inputs.observesIndex;
  };
  env = pkg.env.bin;
in
  makeTemplate {
    name = "observes-singer-tap-checkly-env-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
