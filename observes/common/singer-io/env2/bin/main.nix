# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fetchNixpkgs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath "/observes/common/singer-io";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "observes-common-singer-io-env-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
