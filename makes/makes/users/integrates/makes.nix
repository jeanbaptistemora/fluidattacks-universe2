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
        version = "0.14";
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
        version = "0.14";
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
      gitlab_token = "PRODUCT_API_TOKEN";
      gitlab_token_services = "SERVICES_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersIntegratesKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersIntegratesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersIntegrates"
        ];
        resources = [
          "aws_iam_access_key.integrates-dev-key-1"
          "aws_iam_access_key.integrates-prod-key-1"
        ];
        reDeploy = true;
        src = "/makes/makes/users/integrates/infra";
        version = "0.14";
      };
      makesUsersIntegratesKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersIntegratesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersIntegrates"
        ];
        resources = [
          "aws_iam_access_key.integrates-dev-key-2"
          "aws_iam_access_key.integrates-prod-key-2"
        ];
        reDeploy = true;
        src = "/makes/makes/users/integrates/infra";
        version = "0.14";
      };
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
        version = "0.14";
      };
    };
  };
}
