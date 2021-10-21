{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      airsInfra = {
        setup = [
          outputs."/secretsForAwsFromEnv/airsProd"
          outputs."/secretsForEnvFromSops/airsInfraProd"
          outputs."/secretsForTerraformFromEnv/airsInfra"
        ];
        src = "/airs/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      airsInfra = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/airsInfraDev"
          outputs."/secretsForTerraformFromEnv/airsInfra"
        ];
        src = "/airs/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    airsInfraDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_TOKEN" ];
      manifest = "/airs/secrets/dev.yaml";
    };
    airsInfraProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_TOKEN" ];
      manifest = "/airs/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    airsInfra = {
      cloudflareAccountId = "CLOUDFLARE_ACCOUNT_ID";
      cloudflareApiToken = "CLOUDFLARE_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      airsInfra = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/airsInfraDev"
          outputs."/secretsForTerraformFromEnv/airsInfra"
        ];
        src = "/airs/infra";
        version = "1.0";
      };
    };
  };
}
