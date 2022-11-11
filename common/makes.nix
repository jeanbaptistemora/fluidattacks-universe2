# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{
  imports = [
    ./ci/makes.nix
    ./compute/makes.nix
    ./cluster/makes.nix
    ./criteria/makes.nix
    ./dev/makes.nix
    ./dns/makes.nix
    ./foss/makes.nix
    ./monitoring/makes.nix
    ./okta/makes.nix
    ./pipeline/makes.nix
    ./status/makes.nix
    ./users/makes.nix
    ./vpc/makes.nix
    ./vpn/makes.nix
  ];
  secretsForAwsFromGitlab = {
    dev = {
      roleArn = "arn:aws:iam::205810638802:role/dev";
      duration = 3600;
    };
    prodCommon = {
      roleArn = "arn:aws:iam::205810638802:role/prod_common";
      duration = 3600;
    };
  };
  secretsForEnvFromSops = {
    commonCloudflareDev = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
      ];
      manifest = "/common/secrets/dev.yaml";
    };
    commonCloudflareProd = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
      ];
      manifest = "/common/secrets/prod.yaml";
    };
  };
}
