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
  testTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/envVarsForTerraform/commonCompute"
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
}
