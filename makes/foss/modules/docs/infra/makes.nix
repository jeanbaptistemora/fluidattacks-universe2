{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      docsInfra = {
        setup = [
          outputs."/secretsForAwsFromEnv/docsProd"
          outputs."/secretsForEnvFromSops/docsInfraProd"
          outputs."/secretsForTerraformFromEnv/docsInfra"
        ];
        src = "/docs/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      docsInfra = {
        setup = [
          outputs."/secretsForAwsFromEnv/docsDev"
          outputs."/secretsForEnvFromSops/docsInfraDev"
          outputs."/secretsForTerraformFromEnv/docsInfra"
        ];
        src = "/docs/infra";
        version = "1.0";
      };
    };
  };
  secretsForAwsFromEnv = {
    docsDev = {
      accessKeyId = "DOCS_DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "DOCS_DEV_AWS_SECRET_ACCESS_KEY";
    };
    docsProd = {
      accessKeyId = "DOCS_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "DOCS_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
  secretsForEnvFromSops = {
    docsInfraDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_TOKEN" ];
      manifest = "/docs/secrets/dev.yaml";
    };
    docsInfraProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_TOKEN" ];
      manifest = "/docs/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    docsInfra = {
      cloudflareAccountId = "CLOUDFLARE_ACCOUNT_ID";
      cloudflareApiToken = "CLOUDFLARE_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      docsInfra = {
        setup = [
          outputs."/secretsForAwsFromEnv/docsDev"
          outputs."/secretsForEnvFromSops/docsInfraDev"
          outputs."/secretsForTerraformFromEnv/docsInfra"
        ];
        src = "/docs/infra";
        version = "1.0";
      };
    };
  };
}
