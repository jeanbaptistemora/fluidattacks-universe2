# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersDocs = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersDocsProd"
          outputs."/secretsForTerraformFromEnv/makesUsersDocs"
        ];
        src = "/makes/foss/modules/makes/users/docs/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersDocs = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/foss/modules/makes/users/docs/infra";
        version = "0.14";
      };
    };
  };
  secretsForEnvFromSops = {
    makesUsersDocsDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/dev.yaml";
    };
    makesUsersDocsProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersDocs = {
      gitlab_token = "PRODUCT_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersDocsKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersDocsProd"
          outputs."/secretsForTerraformFromEnv/makesUsersDocs"
        ];
        resources = [
          "aws_iam_access_key.dev_1"
          "aws_iam_access_key.prod_1"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/docs/infra";
        version = "0.14";
      };
      makesUsersDocsKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersDocsProd"
          outputs."/secretsForTerraformFromEnv/makesUsersDocs"
        ];
        resources = [
          "aws_iam_access_key.dev_2"
          "aws_iam_access_key.prod_2"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/docs/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersDocs = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesUsersDocsDev"
          outputs."/secretsForTerraformFromEnv/makesUsersDocs"
        ];
        src = "/makes/foss/modules/makes/users/docs/infra";
        version = "0.14";
      };
    };
  };
}
