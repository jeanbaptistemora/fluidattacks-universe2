# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersSkims = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersSkims"
        ];
        src = "/makes/foss/modules/makes/users/skims/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersSkims = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/foss/modules/makes/users/skims/infra";
        version = "1.0";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersSkims = {
      gitlab_token = "PRODUCT_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersSkimsKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersSkims"
        ];
        resources = [
          "aws_iam_access_key.skims_dev_key-1"
          "aws_iam_access_key.skims_prod_key-1"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/skims/infra";
        version = "1.0";
      };
      makesUsersSkimsKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersSkims"
        ];
        resources = [
          "aws_iam_access_key.skims_dev_key-2"
          "aws_iam_access_key.skims_prod_key-2"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/skims/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersSkims = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersSkims"
        ];
        src = "/makes/foss/modules/makes/users/skims/infra";
        version = "1.0";
      };
    };
  };
}
