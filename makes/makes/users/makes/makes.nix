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
        src = "/makes/makes/users/makes/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersMakes = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/makes/infra";
        version = "0.14";
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
        ];
        reDeploy = true;
        src = "/makes/makes/users/makes/infra";
        version = "0.14";
      };
      makesUsersMakesKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersMakes"
        ];
        resources = [
          "aws_iam_access_key.dev-key-2"
        ];
        reDeploy = true;
        src = "/makes/makes/users/makes/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersMakes = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersMakes"
        ];
        src = "/makes/makes/users/makes/infra";
        version = "0.14";
      };
    };
  };
}
