# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonUsers = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonCloudflareProd"
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
        ];
        src = "/common/users/infra";
        version = "1.0";
      };
    };
  };
}
