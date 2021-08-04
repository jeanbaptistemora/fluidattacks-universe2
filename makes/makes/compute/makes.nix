# https://github.com/fluidattacks/makes
{ outputs
, projectPath
, ...
}:
{
  deployTerraform = {
    modules = {
      makesCompute = {
        setup = [
          outputs."/envVarsForTerraform/makesCompute"
          outputs."/secretsForAwsFromEnv/makesProd"
        ];
        src = "/makes/makes/compute/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesCompute = {
        setup = [
          outputs."/envVarsForTerraform/makesCompute"
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/compute/infra";
        version = "0.14";
      };
    };
  };
  envVarsForTerraform = {
    makesCompute = {
      skimsQueues = projectPath "/skims/manifests/queues.json";
    };
  };
  testTerraform = {
    modules = {
      makesCompute = {
        setup = [
          outputs."/envVarsForTerraform/makesCompute"
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/compute/infra";
        version = "0.14";
      };
    };
  };
}
