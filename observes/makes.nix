# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{projectPath, ...}: {
  imports = [
    ./batch/makes.nix
    ./dev/makes.nix
    ./infra/makes.nix
    ./lint/makes.nix
    ./pipeline/makes.nix
  ];
  inputs = {
    observesIndex = import (projectPath "/observes/architecture/index.nix");
  };
  secretsForAwsFromGitlab = {
    prodObserves = {
      roleArn = "arn:aws:iam::205810638802:role/prod_observes";
      duration = 3600;
    };
  };
}
