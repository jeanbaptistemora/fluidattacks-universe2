# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fetchNixpkgs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath "/observes/common/purity";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "observes-common-purity-env-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
