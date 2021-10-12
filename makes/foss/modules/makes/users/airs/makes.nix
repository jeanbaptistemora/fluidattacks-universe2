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
        src = "/makes/foss/modules/makes/users/airs/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersAirs = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/foss/modules/makes/users/airs/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesUsersAirsDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/dev.yaml";
    };
    makesUsersAirsProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersAirs = {
      gitlab_token = "PRODUCT_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersAirsKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersAirsProd"
          outputs."/secretsForTerraformFromEnv/makesUsersAirs"
        ];
        resources = [
          "aws_iam_access_key.airs-dev-key-1"
          "aws_iam_access_key.airs-prod-key-1"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/airs/infra";
        version = "1.0";
      };
      makesUsersAirsKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersAirsProd"
          outputs."/secretsForTerraformFromEnv/makesUsersAirs"
        ];
        resources = [
          "aws_iam_access_key.airs-dev-key-2"
          "aws_iam_access_key.airs-prod-key-2"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/airs/infra";
        version = "1.0";
      };
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
        src = "/makes/foss/modules/makes/users/airs/infra";
        version = "1.0";
      };
    };
  };
}
