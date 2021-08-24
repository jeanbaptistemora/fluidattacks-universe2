# https://github.com/fluidattacks/makes
{ inputs
, makeDerivation
, outputs
, ...
}:
let
  skimsQueuesAvailable = makeDerivation {
    name = "skims-queues-after-exclusions";
    env.envPrintAvailableQueues = builtins.toFile "print-available-queues.py" ''
      import skims_sdk
      skims_sdk.print_available_queues()
    '';
    searchPaths = {
      bin = [ inputs.nixpkgs.python38 ];
      source = [ inputs.product.skims-config-sdk ];
    };
    builder = "python $envPrintAvailableQueues > $out";
  };
in
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
      skimsQueues = skimsQueuesAvailable.outPath;
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
