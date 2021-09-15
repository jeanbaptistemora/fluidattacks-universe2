# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersSorts"
        ];
        src = "/makes/foss/modules/makes/users/sorts/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersSorts"
        ];
        src = "/makes/foss/modules/makes/users/sorts/infra";
        version = "0.14";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersSorts = {
      gitlab_token = "PRODUCT_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersSortsKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersSorts"
        ];
        resources = [
          "aws_iam_access_key.sorts_dev_key-1"
          "aws_iam_access_key.sorts_prod_key-1"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/sorts/infra";
        version = "0.14";
      };
      makesUsersSortsKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersSorts"
        ];
        resources = [
          "aws_iam_access_key.sorts_dev_key-2"
          "aws_iam_access_key.sorts_prod_key-2"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/sorts/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersSorts"
        ];
        src = "/makes/foss/modules/makes/users/sorts/infra";
        version = "0.14";
      };
    };
  };
}
