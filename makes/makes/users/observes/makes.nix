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
        src = "/makes/makes/users/observes/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersObserves = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/observes/infra";
        version = "0.13";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersObserves = {
      aws_access_key = "AWS_ACCESS_KEY_ID";
      aws_secret_key = "AWS_SECRET_ACCESS_KEY";
      gitlab_token = "PRODUCT_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  testTerraform = {
    modules = {
      makesUsersObserves = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersObserves"
        ];
        src = "/makes/makes/users/observes/infra";
        version = "0.13";
      };
    };
  };
}
