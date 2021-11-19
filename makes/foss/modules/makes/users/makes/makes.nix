# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersMakes = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersMakes"
        ];
        src = "/makes/foss/modules/makes/users/makes/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersMakes = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/makes/users/makes/infra";
        version = "1.0";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersMakes = {
      gitlab_token = "PRODUCT_API_TOKEN";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersMakesKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersMakes"
        ];
        resources = [
          "aws_iam_access_key.dev-key-1"
          "aws_iam_access_key.prod-key-1"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/makes/infra";
        version = "1.0";
      };
      makesUsersMakesKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersMakes"
        ];
        resources = [
          "aws_iam_access_key.dev-key-2"
          "aws_iam_access_key.prod-key-2"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/makes/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersMakes = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/makesUsersMakes"
        ];
        src = "/makes/foss/modules/makes/users/makes/infra";
        version = "1.0";
      };
    };
  };
}
