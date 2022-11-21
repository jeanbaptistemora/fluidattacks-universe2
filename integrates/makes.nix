# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{
  imports = [
    ./back/makes.nix
    ./infra/makes.nix
    ./pipeline/makes.nix
    ./jobs/makes.nix
    ./storage/infra/makes.nix
    ./streams/makes.nix
  ];
  secretsForAwsFromGitlab = {
    prodIntegrates = {
      roleArn = "arn:aws:iam::205810638802:role/prod_integrates";
      duration = 3600;
    };
  };
}
