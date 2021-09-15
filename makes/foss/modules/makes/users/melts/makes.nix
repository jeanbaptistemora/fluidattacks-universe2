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
        src = "/makes/foss/modules/makes/users/melts/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersMelts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/foss/modules/makes/users/melts/infra";
        version = "0.14";
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
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/melts/infra";
        version = "0.14";
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
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/melts/infra";
        version = "0.14";
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
        src = "/makes/foss/modules/makes/users/melts/infra";
        version = "0.14";
      };
    };
  };
}
