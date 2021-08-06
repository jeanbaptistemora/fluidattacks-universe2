# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersAirs = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersAirsProd"
          outputs."/secretsForTerraformFromEnv/makesUsersAirs"
        ];
        src = "/makes/makes/users/airs/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersAirs = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/airs/infra";
        version = "0.13";
      };
    };
  };
  secretsForEnvFromSops = {
    makesUsersAirsDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/makes/secrets/dev.yaml";
    };
    makesUsersAirsProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersAirs = {
      aws_access_key = "AWS_ACCESS_KEY_ID";
      aws_secret_key = "AWS_SECRET_ACCESS_KEY";
      cloudflare_api_key = "CLOUDFLARE_API_KEY";
      cloudflare_email = "CLOUDFLARE_EMAIL";
      region = "AWS_DEFAULT_REGION";
    };
  };
  testTerraform = {
    modules = {
      makesUsersAirs = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesUsersAirsDev"
          outputs."/secretsForTerraformFromEnv/makesUsersAirs"
        ];
        src = "/makes/makes/users/airs/infra";
        version = "0.13";
      };
    };
  };
}
