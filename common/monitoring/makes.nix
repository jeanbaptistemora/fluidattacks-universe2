# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonMonitoring = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonMonitoringOkta"
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
          outputs."/secretsForEnvFromSops/commonMonitoringOkta"
          outputs."/secretsForTerraformFromEnv/commonMonitoring"
        ];
        src = "/common/monitoring/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonMonitoringOkta = {
      vars = ["OKTA_API_TOKEN"];
      manifest = "/common/okta/data.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonMonitoring = {
      oktaApiToken = "OKTA_API_TOKEN";
    };
  };
}
