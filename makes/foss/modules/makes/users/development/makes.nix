# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersDevelopment = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersDevelopmentProd"
          outputs."/secretsForTerraformFromEnv/makesUsersDevelopment"
        ];
        src = "/makes/foss/modules/makes/users/development/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersDevelopment = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/foss/modules/makes/users/development/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesUsersDevelopmentDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/dev.yaml";
    };
    makesUsersDevelopmentProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersDevelopment = {
      gitlab_token = "PRODUCT_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      makesUsersDevelopment = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesUsersDevelopmentDev"
          outputs."/secretsForTerraformFromEnv/makesUsersDevelopment"
        ];
        src = "/makes/foss/modules/makes/users/development/infra";
        version = "1.0";
      };
    };
  };
}
