# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersMelts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersMelts"
        ];
        src = "/makes/makes/users/melts/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersMelts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/melts/infra";
        version = "0.13";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersMelts = {
      gitlab_token = "PRODUCT_API_TOKEN";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersMeltsKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersMelts"
        ];
        resources = [
          "aws_iam_access_key.melts-dev-key-1"
          "aws_iam_access_key.melts-prod-key-1"
        ];
        src = "/makes/makes/users/melts/infra";
        version = "0.13";
      };
      makesUsersMeltsKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersMelts"
        ];
        resources = [
          "aws_iam_access_key.melts-dev-key-2"
          "aws_iam_access_key.melts-prod-key-2"
        ];
        src = "/makes/makes/users/melts/infra";
        version = "0.13";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersMelts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersMelts"
        ];
        src = "/makes/makes/users/melts/infra";
        version = "0.13";
      };
    };
  };
}
