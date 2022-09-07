# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  imports = [
    ./dev/makes.nix
    ./infra/makes.nix
    ./lint/makes.nix
    ./pipeline/makes.nix
    ./test/makes.nix
  ];
  secretsForAwsFromGitlab = {
    prodSorts = {
      roleArn = "arn:aws:iam::205810638802:role/prod_sorts";
      duration = 3600;
    };
  };
}
