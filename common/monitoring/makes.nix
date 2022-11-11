# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonMonitoring = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonMonitoringProd"
          outputs."/secretsForTerraformFromEnv/commonMonitoring"
        ];
        src = "/common/monitoring/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonMonitoring = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
        ];
        src = "/common/monitoring/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      commonMonitoring = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonMonitoringDev"
          outputs."/secretsForTerraformFromEnv/commonMonitoring"
        ];
        src = "/common/monitoring/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonMonitoringDev = {
      vars = ["REDSHIFT_USER" "REDSHIFT_PASSWORD"];
      manifest = "/common/secrets/dev.yaml";
    };
    commonMonitoringProd = {
      vars = ["REDSHIFT_USER" "REDSHIFT_PASSWORD"];
      manifest = "/common/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonMonitoring = {
      redshiftUser = "REDSHIFT_USER";
      redshiftPassword = "REDSHIFT_PASSWORD";
    };
  };
}
