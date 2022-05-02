# https://github.com/fluidattacks/makes
{
  outputs,
  projectPath,
  ...
}: {
  deployTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/envVarsForTerraform/commonCompute"
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForTerraformFromEnv/commonCompute"
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
          outputs."/envVarsForTerraform/commonCompute"
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/commonCompute"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
  envVarsForTerraform = {
    commonCompute = {
      skimsQueues = projectPath "/skims/manifests/queues.json";
    };
  };
  secretsForTerraformFromEnv = {
    commonCompute = {
      productApiToken = "PRODUCT_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/envVarsForTerraform/commonCompute"
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/commonCompute"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
}
