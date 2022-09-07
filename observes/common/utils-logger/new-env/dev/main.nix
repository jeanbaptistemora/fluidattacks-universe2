# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  projectPath,
  fetchNixpkgs,
  ...
}: let
  root = projectPath inputs.observesIndex.common.utils_logger.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.dev;
in
  makeTemplate {
    searchPaths = {
      bin = [env];
    };
    name = "observes-common-utils-logger-new-env-development";
  }
