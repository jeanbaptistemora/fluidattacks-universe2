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
          outputs."/secretsForAwsFromEnv/prodMakes"
        ];
        src = "/makes/foss/modules/makes/compute/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesCompute = {
        setup = [
          outputs."/envVarsForTerraform/makesCompute"
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/makes/compute/infra";
        version = "1.0";
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
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/makes/compute/infra";
        version = "1.0";
      };
    };
  };
}
