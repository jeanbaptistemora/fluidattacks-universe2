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
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      airsInfra = {
        setup = [
          outputs."/secretsForAwsFromEnv/airsDev"
          outputs."/secretsForEnvFromSops/airsInfraDev"
          outputs."/secretsForTerraformFromEnv/airsInfra"
        ];
        src = "/airs/infra";
        version = "0.14";
      };
    };
  };
  secretsForAwsFromEnv = {
    airsDev = {
      accessKeyId = "AIRS_DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "AIRS_DEV_AWS_SECRET_ACCESS_KEY";
    };
    airsProd = {
      accessKeyId = "AIRS_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "AIRS_PROD_AWS_SECRET_ACCESS_KEY";
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
          outputs."/secretsForAwsFromEnv/airsDev"
          outputs."/secretsForEnvFromSops/airsInfraDev"
          outputs."/secretsForTerraformFromEnv/airsInfra"
        ];
        src = "/airs/infra";
        version = "0.14";
      };
    };
  };
}
