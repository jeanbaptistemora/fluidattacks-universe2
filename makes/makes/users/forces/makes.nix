# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersForces = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersForces"
        ];
        src = "/makes/makes/users/forces/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersForces = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/forces/infra";
        version = "0.13";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersForces = {
      aws_access_key = "AWS_ACCESS_KEY_ID";
      aws_secret_key = "AWS_SECRET_ACCESS_KEY";
      gitlab_token = "PRODUCT_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  testTerraform = {
    modules = {
      makesUsersForces = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersForces"
        ];
        src = "/makes/makes/users/forces/infra";
        version = "0.13";
      };
    };
  };
}
