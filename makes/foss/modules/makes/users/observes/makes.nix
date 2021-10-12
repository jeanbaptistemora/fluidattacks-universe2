# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersObserves = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersObserves"
        ];
        src = "/makes/foss/modules/makes/users/observes/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersObserves = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/foss/modules/makes/users/observes/infra";
        version = "1.0";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersObserves = {
      gitlab_token = "PRODUCT_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersObservesKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersObserves"
        ];
        resources = [
          "aws_iam_access_key.dev-key-1"
          "aws_iam_access_key.prod-key-1"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/observes/infra";
        version = "1.0";
      };
      makesUsersObservesKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersObserves"
        ];
        resources = [
          "aws_iam_access_key.dev-key-2"
          "aws_iam_access_key.prod-key-2"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/observes/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersObserves = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersObserves"
        ];
        src = "/makes/foss/modules/makes/users/observes/infra";
        version = "1.0";
      };
    };
  };
}
