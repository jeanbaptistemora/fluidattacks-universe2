# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersDev = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersDevProd"
          outputs."/secretsForTerraformFromEnv/makesUsersDev"
        ];
        src = "/makes/foss/modules/makes/users/dev/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersDev = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/foss/modules/makes/users/dev/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesUsersDevDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/dev.yaml";
    };
    makesUsersDevProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersDev = {
      gitlab_token = "PRODUCT_API_TOKEN";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersDevKey1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersDevProd"
          outputs."/secretsForTerraformFromEnv/makesUsersDev"
        ];
        resources = [ "module.aws.aws_iam_access_key._1" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/dev/infra";
        version = "1.0";
      };
      makesUsersDevKey2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesUsersDevProd"
          outputs."/secretsForTerraformFromEnv/makesUsersDev"
        ];
        resources = [ "module.aws.aws_iam_access_key._2" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/dev/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersDev = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesUsersDevDev"
          outputs."/secretsForTerraformFromEnv/makesUsersDev"
        ];
        src = "/makes/foss/modules/makes/users/dev/infra";
        version = "1.0";
      };
    };
  };
}
