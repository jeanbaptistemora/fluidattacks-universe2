{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesFront = {
        setup = [
          outputs."/secretsForAwsFromEnv/integratesProd"
          outputs."/secretsForEnvFromSops/integratesFrontProd"
          outputs."/secretsForTerraformFromEnv/integratesFront"
        ];
        src = "/makes/foss/modules/integrates/infra/front/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesFront = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/integratesFrontDev"
          outputs."/secretsForTerraformFromEnv/integratesFront"
        ];
        src = "/makes/foss/modules/integrates/infra/front/infra";
        version = "1.0";
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
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/integratesFrontDev"
          outputs."/secretsForTerraformFromEnv/integratesFront"
        ];
        src = "/makes/foss/modules/integrates/infra/front/infra";
        version = "1.0";
      };
    };
  };
}
