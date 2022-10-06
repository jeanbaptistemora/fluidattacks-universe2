# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.checkly.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath fetchNixpkgs;
    observesIndex = inputs.observesIndex;
  };
  check = pkg.check.tests;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-singer-tap-checkly-check-tests";
    entrypoint = "";
  }
