# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fetchNixpkgs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath "/sorts/association-rules";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  check = pkg.check.types;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "sorts-association-rules-check-types";
    entrypoint = "";
  }
