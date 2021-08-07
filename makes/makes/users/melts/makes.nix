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
