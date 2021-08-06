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
      aws_access_key = "AWS_ACCESS_KEY_ID";
      aws_secret_key = "AWS_SECRET_ACCESS_KEY";
      region = "AWS_DEFAULT_REGION";
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
