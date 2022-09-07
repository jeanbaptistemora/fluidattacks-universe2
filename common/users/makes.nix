# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  secretsForTerraformFromEnv = {
    commonUsers = {
      gitlab_token = "UNIVERSE_API_TOKEN";
      gitlab_token_services = "SERVICES_API_TOKEN";
    };
  };
  deployTerraform = {
    modules = {
      commonUsers = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonCloudflareProd"
          outputs."/secretsForTerraformFromEnv/commonUsers"
        ];
        src = "/common/users/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonUsers = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForTerraformFromEnv/commonUsers"
        ];
        src = "/common/users/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      commonUsers = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForTerraformFromEnv/commonUsers"
        ];
        src = "/common/users/infra";
        version = "1.0";
      };
    };
  };
}
