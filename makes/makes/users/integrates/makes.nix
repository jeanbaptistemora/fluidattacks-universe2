# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersIntegrates = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersIntegratesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersIntegrates"
        ];
        src = "/makes/makes/users/integrates/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersIntegrates = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/integrates/infra";
        version = "0.13";
      };
    };
  };
  secretsForEnvFromSops = {
    makesUsersIntegratesDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/makes/secrets/dev.yaml";
    };
    makesUsersIntegratesProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersIntegrates = {
      aws_access_key = "AWS_ACCESS_KEY_ID";
      aws_secret_key = "AWS_SECRET_ACCESS_KEY";
      cloudflare_api_key = "CLOUDFLARE_API_KEY";
      cloudflare_email = "CLOUDFLARE_EMAIL";
      gitlab_token = "PRODUCT_API_TOKEN";
      gitlab_token_services = "SERVICES_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  testTerraform = {
    modules = {
      makesUsersIntegrates = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesUsersIntegratesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersIntegrates"
        ];
        src = "/makes/makes/users/integrates/infra";
        version = "0.13";
      };
    };
  };
}
