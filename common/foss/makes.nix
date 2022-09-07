# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonFoss = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonFossProd"
          outputs."/secretsForTerraformFromEnv/commonFoss"
        ];
        src = "/common/foss/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonFoss = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonFossDev"
          outputs."/secretsForTerraformFromEnv/commonFoss"
        ];
        src = "/common/foss/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonFossDev = {
      vars = ["GITHUB_API_TOKEN"];
      manifest = "/common/secrets/dev.yaml";
    };
    commonFossProd = {
      vars = ["GITHUB_API_TOKEN"];
      manifest = "/common/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonFoss = {
      githubToken = "GITHUB_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      commonFoss = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonFossDev"
          outputs."/secretsForTerraformFromEnv/commonFoss"
        ];
        src = "/common/foss/infra";
        version = "1.0";
      };
    };
  };
}
