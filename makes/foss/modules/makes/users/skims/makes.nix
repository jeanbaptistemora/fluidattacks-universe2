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
        version = "0.14";
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
        version = "0.14";
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
        version = "0.14";
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
        version = "0.14";
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
        version = "0.14";
      };
    };
  };
}
