# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{
  inputs,
  makeSearchPaths,
  outputs,
  ...
}: let
  searchPaths = makeSearchPaths {
    bin = [inputs.nixpkgs.git];
  };
in {
  deployTerraform = {
    modules = {
      commonVpc = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonCloudflareProd"
          outputs."/secretsForTerraformFromEnv/commonVpc"
        ];
        src = "/common/vpc/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonVpc = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForTerraformFromEnv/commonVpc"
        ];
        src = "/common/vpc/infra";
        version = "1.0";
      };
    };
  };
  secretsForTerraformFromEnv = {
    commonVpc = {
      cloudflare_api_key = "CLOUDFLARE_API_KEY";
      cloudflare_email = "CLOUDFLARE_EMAIL";
    };
  };
  testTerraform = {
    modules = {
      commonVpc = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForTerraformFromEnv/commonVpc"
        ];
        src = "/common/vpc/infra";
        version = "1.0";
      };
    };
  };
}
