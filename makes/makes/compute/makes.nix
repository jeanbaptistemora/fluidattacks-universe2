# https://github.com/fluidattacks/makes
{ outputs
, path
, ...
}:
{
  deployTerraform = {
    modules = {
      compute = {
        authentication = [
          outputs."/envVarsForTerraform/makesCompute"
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/compute/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      compute = {
        authentication = [
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
      compute = {
        authentication = [
          outputs."/envVarsForTerraform/makesCompute"
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/compute/infra";
        version = "0.13";
      };
    };
  };
}
