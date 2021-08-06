# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
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
      region = "AWS_DEFAULT_REGION";
    };
  };
}
