# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  system = "x86_64-linux";
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix;
  check = pkg.outputs.packages."${system}".check.tests;
in
  makeTemplate {
    searchPaths = {
      bin = [check];
    };
    name = "observes-etl-dynamo-etl-conf-check-tests";
  }
