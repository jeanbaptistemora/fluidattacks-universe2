# https://github.com/fluidattacks/makes
{ outputs
, path
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
        version = "0.13";
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
        version = "0.13";
      };
    };
  };
  envVarsForTerraform = {
    makesCompute = {
      skimsQueues = path "/skims/manifests/queues.json";
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
        version = "0.13";
      };
    };
  };
}
