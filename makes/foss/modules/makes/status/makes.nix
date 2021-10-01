# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesStatusProd"
          outputs."/secretsForTerraformFromEnv/makesStatus"
        ];
        src = "/makes/foss/modules/makes/status/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesStatusDev"
          outputs."/secretsForTerraformFromEnv/makesStatus"
        ];
        src = "/makes/foss/modules/makes/status/infra";
        version = "0.14";
      };
    };
  };
  secretsForEnvFromSops = {
    makesStatusProd = {
      vars = [ "CHECKLY_API_KEY" ];
      manifest = "/makes/foss/modules/makes/secrets/prod.yaml";
    };
    makesStatusDev = {
      vars = [ "CHECKLY_API_KEY" ];
      manifest = "/makes/foss/modules/makes/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesStatus = {
      checklyApiKey = "CHECKLY_API_KEY";
    };
  };
  testTerraform = {
    modules = {
      makesStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesStatusDev"
          outputs."/secretsForTerraformFromEnv/makesStatus"
        ];
        src = "/makes/foss/modules/makes/status/infra";
        version = "0.14";
      };
    };
  };
}
