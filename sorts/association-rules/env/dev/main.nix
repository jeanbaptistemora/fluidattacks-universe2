# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fetchNixpkgs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath "/sorts/association-rules";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.dev;
in
  makeTemplate {
    name = "sorts-association-rules-env-dev";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
