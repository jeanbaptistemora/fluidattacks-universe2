{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesFront = {
        setup = [
          outputs."/secretsForAwsFromEnv/integratesDev"
          outputs."/secretsForEnvFromSops/integratesFrontProd"
          outputs."/secretsForTerraformFromEnv/integratesFront"
        ];
        src = "/makes/foss/modules/integrates/infra/front/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesFront = {
        setup = [
          outputs."/secretsForAwsFromEnv/integratesDev"
          outputs."/secretsForEnvFromSops/integratesFrontDev"
          outputs."/secretsForTerraformFromEnv/integratesFront"
        ];
        src = "/makes/foss/modules/integrates/infra/front/infra";
        version = "0.14";
      };
    };
  };
  secretsForEnvFromSops = {
    integratesFrontDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_TOKEN" ];
      manifest = "/integrates/secrets-development.yaml";
    };
    integratesFrontProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_TOKEN" ];
      manifest = "/integrates/secrets-production.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    integratesFront = {
      cloudflare_api_token = "CLOUDFLARE_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      integratesFront = {
        setup = [
          outputs."/secretsForAwsFromEnv/integratesDev"
          outputs."/secretsForEnvFromSops/integratesFrontDev"
          outputs."/secretsForTerraformFromEnv/integratesFront"
        ];
        src = "/makes/foss/modules/integrates/infra/front/infra";
        version = "0.14";
      };
    };
  };
}
