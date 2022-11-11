# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{outputs, ...}: {
  imports = [
    ./arch/makes.nix
    ./schedule/makes.nix
  ];
  deployTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonComputeProd"
          outputs."/secretsForTerraformFromEnv/commonCompute"
          outputs."/common/compute/schedule/parse-terraform"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/common/compute/schedule/parse-terraform"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonComputeDev"
          outputs."/secretsForTerraformFromEnv/commonCompute"
          outputs."/common/compute/schedule/parse-terraform"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonComputeDev = {
      vars = ["REDSHIFT_USER" "REDSHIFT_PASSWORD"];
      manifest = "/common/secrets/dev.yaml";
    };
    commonComputeProd = {
      vars = ["REDSHIFT_USER" "REDSHIFT_PASSWORD"];
      manifest = "/common/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonCompute = {
      redshiftUser = "REDSHIFT_USER";
      redshiftPassword = "REDSHIFT_PASSWORD";
    };
  };
}
